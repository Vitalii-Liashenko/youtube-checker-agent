import logging
from datetime import datetime, UTC
from config import DEVELOPER_MODE
from video_info_provider import VideoInfoProvider
from open_ai_checker import OpenAiChecker
from models import VideoCheckResult, Session

logger = logging.getLogger(__name__)


class VideoChecker:
    def __init__(self):
        self.video_info_provider = VideoInfoProvider()
        self.open_ai_checker = OpenAiChecker()

    def is_russian_video(self, video_id):
        if DEVELOPER_MODE:
            return False
        
        session = Session()
        # Перевіряємо кеш
        cached = session.query(VideoCheckResult).filter_by(video_id=video_id).first()
        if cached:
            logger.info(f"Cache hit for video {video_id}: {cached.is_russian}")
            session.close()
            return cached.is_russian

        try:
            channel_id = self.video_info_provider.get_channel_id(video_id)
            channel_info = self.video_info_provider.get_channel_info(channel_id)
            confidenceAboutCountry = 1 # 1 - 100% confidence from Youtube API

            if channel_info.country.upper() != 'RU':
                is_russian, confidence = self.open_ai_checker.get_country(
                    channel_info.channel_title,
                    channel_info.channel_description
                )
                confidenceAboutCountry = confidence
            else:
                is_russian = True

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
            logger.error(f"Error processing video {video_id}: {str(e)}")
            return False
        finally:
            session.close() 