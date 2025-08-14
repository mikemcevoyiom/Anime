import os
import re
from flask import Flask, jsonify
import requests
import feedparser

SONARR_URL = os.environ.get("SONARR_URL", "https://sonarr.manxrallying.uk/api/v3")
FEED_URL = "https://feed.animetosho.org/rss2"

app = Flask(__name__)

def get_missing_episodes():
    headers = {"X-Api-Key": SONARR_API_KEY} if SONARR_API_KEY else {}
    try:
        resp = requests.get(
            f"{SONARR_URL}/wanted/missing",
            params={"includeSeries": "true", "pageSize": 1000},
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        episodes = data.get("records", [])
        missing = []
        for ep in episodes:
            series_title = ep["series"]["title"]
            ep_num = ep["episodeNumber"]
            missing.append({"series": series_title, "episode": ep_num})
        return missing
    except Exception:
        return []

def parse_feed():
    feed = feedparser.parse(FEED_URL)
    entries = []
    pattern = re.compile(r"^(.*?) - (\d+)")
    for e in feed.entries:
        match = pattern.match(e.title)
        if not match:
            continue
        series_title = match.group(1)
        episode = int(match.group(2))
        link = e.enclosures[0]["url"] if e.get("enclosures") else e.link
        entries.append({"series": series_title, "episode": episode, "link": link})
    return entries

@app.route("/")
def index():
    missing = get_missing_episodes()
    feed_entries = parse_feed()
    available = []
    for m in missing:
        for f in feed_entries:
            if f["series"].lower() == m["series"].lower() and f["episode"] == m["episode"]:
                available.append({"series": m["series"], "episode": m["episode"], "link": f["link"]})
    return jsonify(available)

if __name__ == "__main__":
    app.run(debug=True)
