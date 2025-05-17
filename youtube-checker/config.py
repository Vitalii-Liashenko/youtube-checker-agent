import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Server configuration
SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
SERVER_PORT = int(os.getenv('SERVER_PORT', 8080))

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = os.getenv('LOG_FILE', 'app.log')

# API Keys
OPEN_API_KEY = os.getenv('OPEN_API_KEY')

# Developer mode
DEVELOPER_MODE = os.getenv('DEVELOPER_MODE', 'False').lower() == 'true'

# Database configuration
DB_PATH = os.getenv('DB_PATH', 'video_checks.db')

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
DEVELOPER_MODE_DEFAULT_IS_RUSSIAN_VALUE = os.getenv('DEVELOPER_MODE_DEFAULT_IS_RUSSIAN_VALUE', '').lower() == 'true' 