
from tags import all_events
from scrap import fetchAndWrite
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import jsons


app = FastAPI()

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
    #print("city ------>",city)
    url = f"https://insider.in/all-events-in-{city}"
    path = f"data/events/{city}.html"

    try:
        res =  fetchAndWrite(url,path)
        print("res------->", res)
        if not res:
            return {"status": "error", "message": f"❌ Error in fetchAndWrite for {city}"}
    except Exception as e:
        return {"status": "error", "message": f"❌ Error in fetchAndWrite: {str(e)} "}
    
    try:
        city_data = await all_events(city)
        print("city_data------>", city_data)
    except Exception as e:
        return {"status": "error", "message": f"❌ Error in all_events: {str(e)}"}
        #print("city_data------>",city_data)
    city_data_json = jsons.dump(city_data)
        #print("city_data_json------>", city_data_json)
    return {"status": "success", "message": f"Data fetched for {city}", "data":city_data_json}


# #Run with: python -m uvicorn main:app --reload


