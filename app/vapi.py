import os, requests
from dotenv import load_dotenv

load_dotenv()
API_BASE = "https://api.vapi.ai"


VAPI_TOKEN = os.getenv("VAPI_PRIVATE_TOKEN")
DEFAULT_ASSISTANT = os.getenv("VAPI_ASSISTANT_ID")
DEFAULT_PHONE_ID = os.getenv("VAPI_PHONE_NUMBER_ID")

API_BASE = "https://api.vapi.ai"

def place_call(customer_number: str, assistant_id: str | None = None, phone_number_id: str | None = None):
    assert VAPI_TOKEN, "Missing VAPI_PRIVATE_TOKEN"
    payload = {
        "assistantId": assistant_id or DEFAULT_ASSISTANT,
        "phoneNumberId": phone_number_id or DEFAULT_PHONE_ID,
        "customer": {"number": customer_number}
    }
    r = requests.post(f"{API_BASE}/call", json=payload, headers={"Authorization": f"Bearer {VAPI_TOKEN}"}, timeout=30)
    if r.status_code >= 300:
        raise RuntimeError(f"Vapi call error {r.status_code}: {r.text}")
    return r.json()
