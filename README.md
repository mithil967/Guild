# Guild Bot — Render Dashboard (Safe Demo)

This is a clean Render-ready Flask dashboard plus a background demo worker.

## Important
The ZIP you provided contains a mixture of simulation code and account/access data. The existing `main.py` asks for terminal input and contains endless simulated retry loops; `web.py` expects a missing `config.json`; and `vercel.json` points to a missing `app.py`. The included code does **not** demonstrate a working, authorized Free Fire API integration. This replacement therefore provides a working dashboard and a safe background demo worker only. It does not connect to game servers, send guild invitations, or use account tokens.

## Deploy to Render
1. Create a new **Web Service** and connect the GitHub repository containing these files.
2. Runtime: **Python 3**.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app --workers 1 --threads 4 --timeout 120`
5. Add environment variables:
   - `ADMIN_PASSWORD` = choose a long, unique dashboard password
   - `FLASK_SECRET_KEY` = use a long random secret (Render blueprint can generate this)
6. Deploy. Open the service URL, sign in with `ADMIN_PASSWORD`, then start/stop the demo worker.

## Files
- `app.py` — Flask routes and dashboard authentication
- `bot_worker.py` — safe background demo worker
- `templates/` — login and dashboard UI
- `requirements.txt` — Python dependencies
- `render.yaml` — optional Render Blueprint configuration

## Security
Do not upload `access.txt`, `access.txt.bak`, account credentials, tokens, or private keys to GitHub. If those credentials were real and the ZIP was shared, revoke/rotate them.
