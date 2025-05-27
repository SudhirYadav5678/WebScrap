
from tags import all_events
from scrap import fetchAndWrite
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import jsons


app = FastAPI()

allow_origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_credentials=True,
    allow_headers=["Content-Type", "Authorization"],  # Fix: should be a flat list
    expose_headers=["Content-Type", "Authorization"]
)


class City(BaseModel):
    city: str

@app.post("/fetch-city-events")
async def show_data(data: City):
    city = data.city
    #print("city ------>",city)
    url = f"https://insider.in/all-events-in-{city}"
    path = f"data/events/{city}.html"

    try:
        fetchAndWrite(url, path)
        city_data = all_events(city)
        #print("city_data------>",city_data)
        city_data_json = jsons.dump(city_data)
        #print("city_data_json------>", city_data_json)
        return {"status": "success", "message": f"Data fetched for {city}", "data":city_data_json}
    except Exception as e:
        return {"status": "error", "message": f"❌ Error while fetching data: {str(e)}"}


#Run with: python -m uvicorn main:app --reload
