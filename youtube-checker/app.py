from flask import Flask, jsonify, request
import logging
from datetime import datetime, UTC
from dotenv import load_dotenv
from config import SERVER_HOST, SERVER_PORT, LOG_FILE, LOG_FORMAT, LOG_LEVEL
from video_checker import VideoChecker
from models import Session

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
video_checker = VideoChecker()

# Add CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://www.youtube.com')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept, Origin')
    response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Handle OPTIONS requests
@app.route('/info/videos/<video_id>', methods=['OPTIONS'])
def handle_options(video_id):
    response = app.make_default_options_response()
    response.headers.add('Access-Control-Allow-Origin', 'https://www.youtube.com')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept, Origin')
    response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.before_request
def log_request_info():
    logger.info('Request: %s %s', request.method, request.url)
    logger.info('Headers: %s', dict(request.headers))
    if request.is_json:
        logger.info('Body: %s', request.get_json())

@app.after_request
def log_response_info(response):
    logger.info('Response: %s %s', response.status, response.status_code)
    return response

@app.route('/info/videos/<video_id>', methods=['GET'])
def get_video_info(video_id):
    logger.info(f"Processing request for video ID: {video_id}")
    
    try:
        is_russian = video_checker.is_russian_video(video_id)
        response = jsonify({
            "isRussian": is_russian,
            "videoId": video_id,
            "timestamp": datetime.now(UTC).isoformat()
        })
        logger.info(f"Response for video {video_id}: {response.get_json()}")
        return response
    except Exception as e:
        logger.error(f"Error processing video {video_id}: {str(e)}")
        return jsonify({
            "error": "Failed to process video",
            "videoId": video_id
        }), 500

if __name__ == '__main__':
    logger.info(f'Starting YouTube Checker service on {SERVER_HOST}:{SERVER_PORT}...')
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)