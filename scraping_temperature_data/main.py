import sqlite3
from datetime import datetime, timezone
import time
import requests
import selectorlib


URL = "https://programmer100.pythonanywhere.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

YAML_PATH = "extract.yaml"
DATA_PATH = "data.txt"
DB_PATH = "/root/data.db"

conn = sqlite3.connect(DB_PATH)


def scrape(url: str) -> str:
    res = requests.get(url, timeout=10.0, headers=HEADERS)
    source = res.text
    return source


def extract(source: str) -> str:
    extractor = selectorlib.Extractor.from_yaml_file(YAML_PATH)
    value: str = extractor.extract(source)["temperature"]
    return value


def store(value: str):
    now = (
        datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temperatures VALUES(?,?)", (now, int(value)))
    conn.commit()


def main():
    while True:
        source = scrape(URL)
        value = extract(source)
        store(value)
        time.sleep(30.0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        conn.close()
    except Exception:
        conn.close()
