# from tags import all_events
# from scrap import fetchAndWrite
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import jsons

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Change this to your frontend URL in production
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class City(BaseModel):
#     city: str

# @app.post("/fetch-city-events")
# def show_data(data: City):
#     city = data.city
#     #print("city ------>",city)
#     url = f"https://insider.in/all-events-in-{city}"
#     path = f"data/events/{city}.html"

#     try:
#         fetchAndWrite(url, path)
#         city_data = all_events(city)
#         #print("city_data------>",city_data)
#         #city_data_json = jsons(city_data)
#         #print("city_data_json------>",city_data_json)
#         return {"status": "success", "message": f"Data fetched for {city}", "data":f"{city_data}"}
#     except Exception as e:
#         return {"status": "error", "message": f"❌ Error while fetching data: {str(e)}"}
    

#     # python -m uvicorn main:app --reload  


from tags import all_events
from scrap import fetchAndWrite
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://webscrapbackend-8gos.onrender.com/'],
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=["*"],
    allow_credentials=True
)

class City(BaseModel):
    city: str

def serialize_event(event):
    for key, value in event.items():
        if isinstance(value, ObjectId):
            event[key] = str(value)
    return event

@app.post("/fetch-city-events")
def show_data(data: City):
    city = data.city
    url = f"https://insider.in/all-events-in-{city}"
    path = f"data/events/{city}.html"

    try:
        fetchAndWrite(url, path)
        city_data = all_events(city)

        serialized_data = [serialize_event(event) for event in city_data]
        #print(serialized_data)
        return JSONResponse(content={
            "status": "success",
            "message": f"Data fetched for {city}",
            "data": serialized_data
        })

    except Exception as e:
        return {"status": "error", "message": f"❌ Error while fetching data: {str(e)}"}
