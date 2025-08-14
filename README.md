# Anime Missing Episodes Viewer

A simple Flask web page that lists series with missing episodes from a Sonarr instance.

## Configuration

The app uses the following environment variables:

- `SONARR_URL` – Base URL of the Sonarr instance. Defaults to `https://sonarr.manxrallying.uk`.
- `SONARR_API_KEY` – API key for Sonarr. Defaults to `88072cfcffd64b9fb09967534795d361`.

## Running

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000/` to view the list of series with missing episodes.
