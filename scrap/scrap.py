import os
import time
import requests
import httpx

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



def fetchAndWrite(url: str, path: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ HTML fetched and written to {path}")
        return True
    except requests.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        return False