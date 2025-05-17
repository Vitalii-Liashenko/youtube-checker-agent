import logging
from dataclasses import dataclass
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import YOUTUBE_API_KEY, DEVELOPER_MODE

logger = logging.getLogger(__name__)

@dataclass
class ChannelInfo:
    country: str
    channel_title: str
    channel_description: str

class VideoInfoProvider:
    def __init__(self):
        self.youtube = None
        if not DEVELOPER_MODE:
            try:
                self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
                logger.info("YouTube API client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize YouTube API client: {str(e)}")

    def get_channel_id(self, video_id):
        try:
            video_response = self.youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            logger.info(f"Fetching video details for ID: {video_id}")
            
            if not video_response['items']:
                logger.warning(f"Video not found: {video_id}")
                return False
                
            video_details = video_response['items'][0]['snippet']
            channel_id = video_details['channelId']
            
            logger.info(f"Fetching channel details for channel ID: {channel_id}") 
            return channel_id    
        except HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False

    def get_channel_info(self, channel_id):
        try:
            # Get channel information
            channel_response = self.youtube.channels().list(
                part='snippet',
                id=channel_id
            ).execute()
            
            if not channel_response['items']:
                logger.warning(f"Channel not found: {channel_id}")
                return False
                
            channel_details = channel_response['items'][0]['snippet']
            country = channel_details.get('country', '')
            channel_title = channel_details.get('title', '')
            channel_description = channel_details.get('description', '')
            
            logger.info(f"Channel ({channel_id}) country: {country}, title: {channel_title}, description: {channel_description}")
            
            return ChannelInfo(country, channel_title, channel_description)
            
        except HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False
