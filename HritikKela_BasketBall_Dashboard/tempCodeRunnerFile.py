from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
import requests
from fastapi.staticfiles import StaticFiles



app = FastAPI()

# API Key
API_KEY = "1381033e-2e47-4ec3-aac5-33c21ee7c6d8"
HEADERS = {"Authorization": API_KEY}

# API Endpoints
ENDPOINTS = {
    "Teams": "https://api.balldontlie.io/v1/teams",
    "Players": "https://api.balldontlie.io/v1/players",
    "Games": "https://api.balldontlie.io/v1/games"
}

# Jinja2 Templates and Static Files
templates = Jinja2Templates(directory="templates")
# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Function to fetch data from API
def fetch_data(url, params=None):
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/players", response_class=HTMLResponse)
async def players_page(request: Request):
    players = fetch_data(ENDPOINTS["Players"], params={"per_page": 20, "page": 1})["data"]
    return templates.TemplateResponse("players.html", {"request": request, "players": players})


@app.get("/teams", response_class=HTMLResponse)
async def teams_page(request: Request):
    teams = fetch_data(ENDPOINTS["Teams"])["data"]
    return templates.TemplateResponse("teams.html", {"request": request, "teams": teams})


@app.get("/stats", response_class=HTMLResponse)
async def stats_page(request: Request):
    players = fetch_data(ENDPOINTS["Players"], params={"per_page": 50, "page": 1})["data"]
    games = fetch_data(ENDPOINTS["Games"], params={"per_page": 50, "seasons[]": 2023})["data"]
    teams = fetch_data(ENDPOINTS["Teams"])["data"]

    total_home_score = sum(game["home_team_score"] for game in games)
    total_visitor_score = sum(game["visitor_team_score"] for game in games)
    avg_home_score = total_home_score / len(games) if games else 0
    avg_visitor_score = total_visitor_score / len(games) if games else 0

    total_weight = sum(int(player["weight"]) for player in players if player["weight"].isdigit())
    avg_weight = total_weight / len(players) if players else 0

    positions = {}
    for player in players:
        position = player["position"] or "Unknown"
        positions[position] = positions.get(position, 0) + 1

    return templates.TemplateResponse(
        "stats.html",
        {
            "request": request,
            "avg_home_score": avg_home_score,
            "avg_visitor_score": avg_visitor_score,
            "avg_weight": avg_weight,
            "positions": positions,
            "teams": teams
        }
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)

