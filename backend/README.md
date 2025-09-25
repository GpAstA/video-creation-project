Backend skeleton for Video Creation Project

Run locally:

1. Create venv and install:

python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt

2. Run:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
