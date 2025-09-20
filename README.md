# Gynae Voice Agent (FastAPI + Vapi)

## Run (dev)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Expose (dev)
```bash
ngrok http 8000
```

## Configure Vapi
- Assistant: paste the prompt (see below) & publish
- Tools (HTTP): point to your server endpoints
- Server URL (webhooks): https://<ngrok>/vapi/webhook
- Attach a phone number to the assistant for inbound

## Test outbound
```bash
curl -X POST http://localhost:8000/call_out   -H 'Content-Type: application/json'   -d '{"customerNumber":"+923001112223"}'
```

## DB
Creates ./gynae.db (SQLite). Tables: patients, appointments, calls.
