import os
from flask import Flask, render_template
import requests

app = Flask(__name__)

API_KEY = os.getenv("SONARR_API_KEY", "88072cfcffd64b9fb09967534795d361")
SONARR_URL = os.getenv("SONARR_URL", "https://sonarr.manxrallying.uk")

@app.route("/")
def index():
    url = f"{SONARR_URL}/api/v3/wanted/missing?includeSeries=true"
    try:
        resp = requests.get(url, headers={"X-Api-Key": API_KEY})
        resp.raise_for_status()
        data = resp.json()
        series = {}
        for item in data.get("records", []):
            s = item.get("series")
            if s:
                series[s["id"]] = s["title"]
        series_list = sorted(series.values())
    except Exception as e:
        series_list = [f"Error fetching data: {e}"]
    return render_template("index.html", series=series_list)

if __name__ == "__main__":
    app.run(debug=True)
