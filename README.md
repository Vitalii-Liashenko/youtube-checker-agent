# YouTube Channel Checker

An agent service that checks if a YouTube video is from a Russian channel. If the video belongs to Russian channel, the extension will show warning on the top of the page and click `next` button on YouTube video page in 1 second. If a user clicks somewhere on the page, the extension will not go to the next video but the warning still will be visible.
This agent may be useful for those people who watch YouTube videos in autoplay mode and want to skip Russian channels without any manual action.
Some YouTube channels don't contain info about countries or sometimes Russian owners use other countries in their channels. In this case, the extension will use OpenAI to analyze the channel and determine if it is Russian.
For example: 
- popular Russian YouTuber's channel 'вДудь' is owned by Russian person but this channel marked as 'ES' (Spain) on YouTube. In this case, the extension will use OpenAI to analyze the channel by it's title and description and determine that it is Russian and skip it in your playlist. Under the hood, the server will store this result in SQLite database with short description about its assumptions regarding made decision and its confidence score.
- Russian channel 'Россия23' marked as 'RU' (Russia) on YouTube. In this case, the extension will not use OpenAI but also skip it in your playlist.
- some channels like 'Антизомби | Гражданская Оборона' don't contain info about countries on YouTube but they are not Russian channels. In this case, the extension will use OpenAI to analyze the channel by it's title and description and determine that it is not Russian and not skip it in your playlist.
- all other channels will not be skipped.

## Features

- **Checks YouTube videos for Russian channel ownership:**
  - Analyzes video content and metadata
  - Uses OpenAI GPT for intelligent channel analysis
  - Caches results in SQLite database
  - REST API endpoint for video checking

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Vitalii-Liashenko/youtube-checker-agent.git
cd youtube-checker-agent/youtube-checker
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` file with your configuration (in root of youtube-checker folder):

```env
YOUTUBE_API_KEY=your_youtube_api_key
OPEN_API_KEY=your_openai_api_key
SERVER_HOST=localhost
SERVER_PORT=5000
LOG_LEVEL=INFO
LOG_FILE=app.log
DEVELOPER_MODE=False # Optional: use this mode when you are developing the Chrome extension and want to use certain responses from the server 
DEVELOPER_MODE_DEFAULT_RESPONSE=true # Optional: change this value to 'true' to return 'true' by default in developer mode
DB_PATH=video_checks.db  # Optional: specify custom database path
```

## How to use

1. Run the server:

```bash
python app.py
```
2. Install the extension in Chrome browser:
   - Open Chrome browser
   - Go to chrome://extensions/
   - Enable "Developer mode"
   - Click "Load unpacked" and select the folder with the extension

## Project structure
youtube-autoplay-extension/
- `manifest.json` - Chrome extension manifest file
- `popup/popup.html` - Chrome extension popup file
- `popup/popup.js` - Chrome extension popup script
- `content/content.js` - Chrome extension content script
youtube-checker/
- `app.py` - Main application file
- `video_checker.py` - Video checker module
- `video_info_provider.py` - YouTube video information provider
- `open_ai_checker.py` - OpenAI checker module
- `models.py` - Database models
- `config.py` - Configuration file
- `.env` - Environment variables file

## Requirements

- Python 3.8+
- Access to OpenAI API
- Chrome browser
- YouTube account

## Future plans

- use real database for possibility of analyzing more videos and making more accurate decisions
- analyze already collected analyzed data to make more accurate decisions
- add possibility to use other models for analysis
- add possibility to filter short videos also
- add possibility to tune filters for video channels - not only Russian channels but also some other undesirble content
- add possibility to use more than one model for analysis
- add user and app metrics collection

## License

MIT
