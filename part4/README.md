<div align="center">

#    HBnB — Part 4: Simple Web Client

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white&style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.x-000?logo=flask&logoColor=white&style=for-the-badge)
![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-2ea44f?style=for-the-badge)

<i>Static frontend that consumes the HBnB API, plus a small sandbox backend for local testing.</i>

</div>

##    Overview
- Purpose: Use a static frontend (Front) to interact with the HBnB API. You can point it at the Part 3 backend (`http://127.0.0.1:5000`) or run the local Part 4 Back server.
- Tech:
  - Front: Plain HTML/CSS/JS (no build step).
  - Back: Flask + Flask-RESTX, mirroring Part 3’s structure for isolated testing.

##    File Tree
```
part4/
  README.md                  # This file
  Front/                     # Static frontend
    index.html               # Home: list/browse places
    place.html               # Place details view
    login.html               # Simple login/register UI (client-side)
    add_review.html          # Form to submit reviews
    scripts.js               # API calls + DOM logic
    styles.css               # Frontend styles
    images/                  # Static assets

  Back/                      # Optional local API server for Part 4
    run.py                   # Flask entrypoint
    main.py                  # Alternative launcher/helper
    config.py                # Config (env, DB URI, etc.)
    requirements.txt         # Python deps for Back
    test.db                  # SQLite DB (dev)
    instance/                # Flask instance folder (runtime files)
    sql/                     # SQL helpers/init scripts
    app/
      __init__.py            # App factory + API registration
      api/                   # API namespaces (v1: users, places, reviews, amenities)
      models/                # Data models
      persistence/           # Repository layer
      services/              # Business logic (facade)
```

##    Quick Start

### Option A — Use Part 3 backend (recommended)
1) Start the Part 4 server:
```bash
cd /home/jimmy/c27/holbertonschool-hbnb/part4/Back
source .venv/bin/activate
python3 run.py
```
2) Serve the frontend (any static server works):
```bash
cd /home/jimmy/c27/holbertonschool-hbnb/part4/Front
python3 -m http.server 8000
```
3) Open: `http://127.0.0.1:8000/index.html`

### Option B — Use the local Part 4 Back server (sandbox)
1) Create venv and install deps:
```bash
cd /home/zekki/holbertonschool-hbnb-1/part4/Back
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2) Run the server:
```bash
python3 run.py
```
By default it listens on `http://127.0.0.1:5000`.

3) Serve the frontend (same as above) and browse to `http://127.0.0.1:8000`.

##    Frontend Config
- API Base URL: `Front/scripts.js` expects `http://127.0.0.1:5000/api/v1` by default.
- If your backend runs elsewhere, update the base URL near the top of `scripts.js`.

##    API Smoke Tests (curl)
- Create user:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Ana","last_name":"Gomez","email":"ana@example.com"}'
```
- List places:
```bash
curl http://127.0.0.1:5000/api/v1/places/
```
- List amenities:
```bash
curl http://127.0.0.1:5000/api/v1/amenities/
```
- List reviews:
```bash
curl http://127.0.0.1:5000/api/v1/reviews/
```

##    Troubleshooting
- “Not Found” page in browser:
  - You may be requesting a route the backend doesn’t define.
  - Confirm the API base URL in `Front/scripts.js` matches your backend.
  - Watch the trailing slash: many endpoints end with `/` (e.g., `/api/v1/users/`).
  - Ensure the server is running and check terminal logs for requests.
  - If using Part 4 Back, verify blueprints are registered under `/api/v1` in `Back/app/__init__.py`.

- CORS errors (browser console):
  - Ensure `flask-cors` is installed and enabled on the backend.
  - Typical setup in the app factory:
    ```python
    from flask_cors import CORS
    CORS(app)
    ```

##    Notes
- The Part 4 Front consumes the same API surface as Part 3. The Part 4 Back mirrors the structure to allow quick, isolated testing without touching Part 3.
- If you change endpoints or payload shapes, update `Front/scripts.js` accordingly.
