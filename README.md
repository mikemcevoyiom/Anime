# Anime Missing Episodes Viewer

A simple Flask web page that lists missing episodes from a Sonarr instance and
checks [AnimeTosho's RSS feed](https://feed.animetosho.org) for matching NZB
downloads.

## Configuration

The app uses the following environment variables:

- `SONARR_URL` – Base URL of the Sonarr instance. Defaults to `https://sonarr.manxrallying.uk`.
- `SONARR_API_KEY` – API key for Sonarr. Defaults to `88072cfcffd64b9fb09967534795d361`.

## Running

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000/` to view missing episodes along with any NZB links
found via AnimeTosho's feed.
