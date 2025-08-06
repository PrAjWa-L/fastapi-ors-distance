# FastAPI ORS Distance API

This FastAPI app calculates driving distance between two coordinates using the OpenRouteService API.

## Endpoint

**POST** `/get-distance/`

**Request:**
```json
{
  "start": [12.9662635, 77.5417072],
  "end": [12.9715330, 77.5079758]
}
```

**Response:**
```json
{
  "distance_km": 327.27
}
```

**Setup**

***1. Install Requirements***
```bash
pip install fastapi uvicorn python-dotenv requests
```
***2. Add your .env:***
```bash
ORS_API_KEY=your_api_key_here
```
***3. Run***
```bash
uvicorn main:app --reload
```
