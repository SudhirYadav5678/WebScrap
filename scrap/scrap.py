import os
import time
import requests

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


async def fetchAndWrite(url, path):
    time.sleep(2)
    try:
        r = requests.get(url)
        r.raise_for_status()

        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(r.text)

        print(f"Saved to {path}")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

