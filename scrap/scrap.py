import os
import time
import requests
import httpx

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



def fetchAndWrite(url: str,path):
    try:
        r = requests.get(url)
        with open(path,"w") as f:
            f.write(r.text) # Raise an error for bad responses
        print(f"✅ HTML fetched and written to {path}")
        return True
    except requests.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        return False