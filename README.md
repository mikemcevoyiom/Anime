# Anime

Simple Flask app to monitor missing anime episodes in Sonarr against the Animetosho RSS feed.

## Setup

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Provide your Sonarr API key and optional URL via environment variables:
   - **Linux/macOS**
     ```bash
     export SONARR_API_KEY="88072cfcffd64b9fb09967534795d361"
     export SONARR_URL="https://sonarr.manxrallying.uk/api/v3"  # optional
     ```
   - **Windows PowerShell**
     ```powershell
     $env:SONARR_API_KEY='88072cfcffd64b9fb09967534795d361'
     $env:SONARR_URL='https://sonarr.manxrallying.uk/api/v3'  # optional
     # persist for future sessions
     setx SONARR_API_KEY '88072cfcffd64b9fb09967534795d361'
     setx SONARR_URL 'https://sonarr.manxrallying.uk/api/v3'
     ```
3. Run the app
   ```bash
   python app.py
   ```

Open `http://localhost:5000/` to view NZB links for missing episodes.
