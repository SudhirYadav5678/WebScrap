import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from bs4 import BeautifulSoup


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def all_events(city: str) -> str:
    print("📂 Parsing events for city:", city)
    events = []

    try:
        with open(f"data/events/{city}.html", "r", encoding="utf-8") as f:
            raw_html = f.read()
    except FileNotFoundError:
        print(f"❌ File for city '{city}' not found.")
        return json.dumps([])

    soup = BeautifulSoup(raw_html, 'html5lib')
    pretty_html = soup.prettify()

    with open(f"data/events/{city}_pretty.html", "w", encoding="utf-8") as f:
        f.write(pretty_html)
    print(f"📝 Prettified HTML saved to data/events/{city}_pretty.html")
    soup = BeautifulSoup(pretty_html, 'html5lib')

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

    #print("events--------->",events)
    return events


if __name__ == "__main__":
    city_name = "goa"
    json_data = all_events(city_name)
    #print(json_data)
