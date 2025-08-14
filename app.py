import os
from flask import Flask, render_template
import requests
import feedparser

app = Flask(__name__)

API_KEY = os.getenv("SONARR_API_KEY", "88072cfcffd64b9fb09967534795d361")
SONARR_URL = os.getenv("SONARR_URL", "https://sonarr.manxrallying.uk")


def search_animetosho(title: str, season: int, episode: int):
    """Search AnimeTosho's RSS feed for NZB links."""
    query = f"{title} {episode:02d}"
    try:
        resp = requests.get(
            "https://feed.animetosho.org/api",
            params={"t": "search", "q": query},
            timeout=10,
        )
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)
        results = []
        for entry in feed.entries:
            nzb_url = None
            for link in entry.get("links", []):
                if link.get("type") == "application/x-nzb" and link.get("href"):
                    nzb_url = link["href"]
                    break
            if nzb_url:
                results.append({"title": entry.get("title"), "url": nzb_url})
        return results
    except Exception:
        return []


@app.route("/")
def index():
    url = f"{SONARR_URL}/api/v3/wanted/missing?includeSeries=true&includeEpisode=true&pageSize=25"
    episodes = []
    error = None
    try:
        resp = requests.get(url, headers={"X-Api-Key": API_KEY}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        for rec in data.get("records", []):
            series = rec.get("series") or {}
            ep = rec.get("episode") or {}
            title = series.get("title")
            season = ep.get("seasonNumber")
            episode_num = ep.get("episodeNumber")
            if not title or season is None or episode_num is None:
                continue
            nzbs = search_animetosho(title, season, episode_num)
            if nzbs:
                episodes.append(
                    {
                        "series": title,
                        "season": season,
                        "episode": episode_num,
                        "nzb_links": nzbs,
                    }
                )
    except Exception as e:
        error = f"Error fetching data: {e}"
    return render_template("index.html", episodes=episodes, error=error)


if __name__ == "__main__":
    app.run(debug=True)
