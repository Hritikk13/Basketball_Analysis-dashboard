from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# API Key
API_KEY = "1381033e-2e47-4ec3-aac5-33c21ee7c6d8"
HEADERS = {"Authorization": API_KEY}

# Endpoint for Teams
TEAMS_URL = "https://api.balldontlie.io/v1/teams"


@app.get("/test-teams")
def test_teams_endpoint():
    try:
        # Make a GET request
        response = requests.get(TEAMS_URL, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse and return the JSON response
        return {"message": "Successfully fetched Teams data", "data": response.json()}
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as err:
        print(f"Other error occurred: {err}")
        raise HTTPException(status_code=500, detail=str(err))
