import os
import time
import requests
import httpx

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


async def fetchHtml(url):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            r.raise_for_status()
        print(f"Fetched HTML from {url}")
        return r.text
    except httpx.RequestError as e:
        print(f"Error fetching {url}: {e}")
        return None
