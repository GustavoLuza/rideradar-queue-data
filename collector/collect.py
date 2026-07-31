import json
import os
import urllib.request
from datetime import datetime, timezone

COLLECTOR_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(COLLECTOR_DIR)
CONFIG_PATH = os.path.join(COLLECTOR_DIR, "parks.json")
DATA_DIR = os.path.join(REPO_DIR, "data")
USER_AGENT = "RideRadar-collector/1.0 (personal non-commercial project; https://queue-times.com)"


def fetch_json(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def flatten_rides(payload):
    rides = []
    for land in payload.get("lands", []):
        land_name = land.get("name", "")
        for ride in land.get("rides", []):
            rides.append((land_name, ride))
    for ride in payload.get("rides", []):
        rides.append(("", ride))
    return rides


def csv_field(value):
    return str(value).replace(",", ";").replace("\n", " ").strip()


def collect():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CONFIG_PATH, encoding="utf-8") as f:
        parks = json.load(f)["parks"]

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    for park in parks:
        park_id = park["id"]
        url = f"https://queue-times.com/parks/{park_id}/queue_times.json"
        try:
            payload = fetch_json(url)
        except Exception as exc:
            print(f"[warn] failed to fetch park {park_id} ({park['name']}): {exc}")
            continue

        rides = flatten_rides(payload)
        out_path = os.path.join(DATA_DIR, f"{park_id}.csv")
        is_new = not os.path.exists(out_path)
        with open(out_path, "a", encoding="utf-8") as f:
            if is_new:
                f.write("timestamp_utc,land,ride_id,ride_name,is_open,wait_time\n")
            for land_name, ride in rides:
                row = [
                    now,
                    csv_field(land_name),
                    csv_field(ride.get("id", "")),
                    csv_field(ride.get("name", "")),
                    csv_field(ride.get("is_open", "")),
                    csv_field(ride.get("wait_time", "")),
                ]
                f.write(",".join(row) + "\n")

        print(f"[ok] {park['name']} ({park_id}): {len(rides)} rides logged")


if __name__ == "__main__":
    collect()
