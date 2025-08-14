# Anime

Simple Flask app to monitor missing anime episodes in Sonarr against the Animetosho RSS feed.

## Setup

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Provide your Sonarr API key and optional URL via environment variables:
   ```bash
   export SONARR_API_KEY="yourkey"
   export SONARR_URL="https://sonarr.manxrallying.uk/api/v3"  # optional
   ```
3. Run the app
   ```bash
   python app.py
   ```

Open `http://localhost:5000/` to view NZB links for missing episodes.
