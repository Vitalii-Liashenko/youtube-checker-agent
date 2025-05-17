# YouTube Russian Channel Checker

An agent service that checks if a YouTube video is from a Russian channel using OpenAI's GPT model.


## Features

- Checks YouTube videos for Russian channel ownership
- Uses OpenAI GPT for intelligent channel analysis
- Caches results in SQLite database
- REST API endpoint for video checking

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```
install `youtube-autoplay-extension` to your Chrome browser

2. Create `.env` file with your configuration (in root of youtube-checker folder):
```
OPEN_API_KEY=your_openai_api_key
SERVER_HOST=localhost
SERVER_PORT=5000
LOG_LEVEL=INFO
LOG_FILE=app.log
DEVELOPER_MODE=False
DB_PATH=video_checks.db  # Optional: specify custom database path
```

3. Run the server:
```bash
python app.py
```

## API Usage

Check a video:
```
GET /info/videos/{video_id}
```

Response:
```json
{
    "isRussian": true/false,
    "videoId": "video_id",
    "timestamp": "2024-05-17T20:15:16.252Z"
}
```

## License

MIT