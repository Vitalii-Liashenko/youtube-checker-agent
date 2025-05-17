import logging
from datetime import datetime, UTC
from typing import Optional
from config import DEVELOPER_MODE
from video_info_provider import VideoInfoProvider
from open_ai_checker import OpenAiChecker
from models import VideoCheckResult, Session
from sqlalchemy.orm import Session as SessionType

logger = logging.getLogger(__name__)

class VideoChecker:
    def __init__(self):
        self.video_info_provider = VideoInfoProvider()
        self.open_ai_checker = OpenAiChecker()

    def __enter__(self):
        self._session = Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            self._session.close()

    def is_russian_video(self, video_id: str) -> bool:
        """
        Determines if a video is Russian based on channel information.
        
        Args:
            video_id: YouTube video ID to check
            
        Returns:
            bool: True if the video is determined to be Russian, False otherwise
        """
        if DEVELOPER_MODE:
            logger.debug("Developer mode enabled - returning False")
            return False

        session = self._session or Session()
        try:
            # Check cache first
            cached = session.query(VideoCheckResult).filter_by(video_id=video_id).first()
            if cached:
                logger.info(f"Cache hit for video {video_id}: {cached.is_russian}")
                return cached.is_russian

            # Get channel information
            channel_id = self.video_info_provider.get_channel_id(video_id)
            if not channel_id:
                logger.error(f"Failed to get channel ID for video {video_id}")
                return False

            channel_info = self.video_info_provider.get_channel_info(channel_id)
            if not channel_info:
                logger.error(f"Failed to get channel info for channel {channel_id}")
                return False

            # Determine if Russian based on country
            confidenceAboutCountry = 1.0  # Confidence from YouTube API
            if channel_info.country.upper() != 'RU':
                try:
                    is_russian, confidence = self.open_ai_checker.get_country(
                        channel_info.channel_title,
                        channel_info.channel_description
                    )
                    confidenceAboutCountry = confidence
                except Exception as e:
                    logger.error(f"OpenAI check failed for channel {channel_id}: {str(e)}")
                    return False
            else:
                is_russian = True

            # Save result to cache
            new_result = VideoCheckResult(
                video_id=video_id,
                is_russian=is_russian,
                channel_title=channel_info.channel_title,
                channel_description=channel_info.channel_description,
                checked_at=datetime.now(UTC),
                confidence=confidenceAboutCountry,
                country=channel_info.country
            )
            session.add(new_result)
            session.commit()
            logger.info(f"Saved result for video {video_id} to cache: {is_russian}")
            return is_russian

        except Exception as e:
            logger.error(
                f"Error processing video {video_id}: {str(e)}",
                exc_info=True
            )
            return False
        finally:
            if not self._session:
                session.close() if session else None