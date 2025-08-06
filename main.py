from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")

app = FastAPI()


class RouteRequest(BaseModel):
    start: list  
    end: list    

def ensure_lonlat(coord):
    """
    Ensure the coordinate is in [longitude, latitude] format.
    If the first number looks like a latitude, we assume it's [lat, lon] and flip it.
    """
    if abs(coord[0]) <= 90 and abs(coord[1]) <= 180:
        return [coord[1], coord[0]]  # Flip to [lon, lat]
    return coord


@app.post("/get-distance/")
def get_distance(request: RouteRequest):
    start = ensure_lonlat(request.start)
    end = ensure_lonlat(request.end)

    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "coordinates": [start, end]
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        distance_km = round(data['routes'][0]['summary']['distance'] / 1000, 2)
        return {"distance_km": distance_km}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail="Invalid response from ORS API")
