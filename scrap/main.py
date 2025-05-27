
# from tags import all_events
# from scrap import fetchAndWrite
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import os
# import jsons


# app = FastAPI()

# origins = [
#     "http://localhost:5173",
#     "http://localhost:5000",
#     "https://web-scrap-u43o.vercel.app"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # allow_origins = os.getenv("CORS_ORIGINS", "*").split(",")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=allow_origins,
# #     allow_methods=["GET", "POST", "PUT", "DELETE"],
# #     allow_credentials=True,
# #     allow_headers=["Content-Type", "Authorization"],  # Fix: should be a flat list
# #     expose_headers=["Content-Type", "Authorization"]
# # )


# class City(BaseModel):
#     city: str

# @app.post("/fetch-city-events")
# async def show_data(data: City):
#     city = data.city
#     #print("city ------>",city)
#     url = f"https://insider.in/all-events-in-{city}"
#     path = f"data/events/{city}.html"

#     try:
#         await fetchAndWrite(url, path)
#         city_data = await all_events(city)
#         #print("city_data------>",city_data)
#         city_data_json = jsons.dump(city_data)
#         #print("city_data_json------>", city_data_json)
#         return {"status": "success", "message": f"Data fetched for {city}", "data":city_data_json}
#     except Exception as e:
#         return {"status": "error", "message": f"❌ Error while fetching data: {str(e)}"}


# #Run with: python -m uvicorn main:app --reload


from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
import httpx
import os
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
import jsons

load_dotenv()

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

origins = [
    "http://localhost:5173",
    "http://localhost:5000",
    "https://web-scrap-u43o.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class City(BaseModel):
    city: str


@app.post("/fetch-city-events")
async def show_data(data: City):
    city = data.city
    url = f"https://insider.in/all-events-in-{city}"

    try:
        raw_html = await fetch_html(url)
        city_data = await parse_events(city, raw_html)

        return {
            "status": "success",
            "message": f"Data fetched for {city}",
            "data": jsons.dump(city_data)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"❌ Error while fetching data: {str(e)}"
        }


async def fetch_html(url: str) -> str:
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/39.0.2171.95 Safari/537.36'
        )
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.text


async def parse_events(city: str, raw_html: str):
    print(f"📂 Parsing events for city: {city}")
    events = []

    soup = BeautifulSoup(raw_html, 'html5lib')
    event_cards = soup.select('div[data-ref="event_card"]')

    for card in event_cards:
        try:
            title = card.select_one('[data-ref="event_card_title"]')
            date_time = card.select_one('[data-ref="event_card_date_string"] p')
            location = card.select_one('[data-ref="event_card_location"] p')
            price = card.select_one(".css-1sh8h77")
            image_tag = card.select_one('img[data-ref="event_card_image"]')
            link_tag = card.find('a')

            event = {
                "City": city,
                "Title": title.text.strip() if title else None,
                "Date_Time": date_time.text.strip() if date_time else None,
                "Location": location.text.strip() if location else None,
                "Price": price.text.strip() if price else None,
                "ImageURL": image_tag['src'] if image_tag and image_tag.has_attr('src') else None,
                "Link": link_tag['href'] if link_tag and link_tag.has_attr('href') else None,
            }
            events.append(event)
        except Exception as e:
            print("⚠️ Error processing card:", e)

    print(f"✅ Parsed {len(events)} events for city: {city}")

    if events:
        collection.delete_many({"City": city})
        collection.insert_many(events)
        print(f"✅ Inserted {len(events)} events into MongoDB.")

    return events
