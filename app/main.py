from dotenv import load_dotenv
load_dotenv() 

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .db import init_db
from .tools import router as tools_router
from .webhook import router as webhook_router
from .scheduler import start_scheduler
from .vapi import place_call
from .schemas import OutboundRequest
from .scheduler import start_scheduler, run_checkins_now
from .db import SessionLocal
from .models import CallLog
from .scheduler import start_scheduler, run_checkins_now
from .admin import router as admin_router



load_dotenv()
init_db()

app = FastAPI(title="Gynae Voice Agent")
app.include_router(admin_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


app.include_router(tools_router)
app.include_router(webhook_router)

@app.get("/")
def root():
    return {"ok": True, "app": "gynae-agent"}

@app.on_event("startup")
def on_start():
    start_scheduler()

@app.post("/call_out")
def call_out(body: OutboundRequest):
    data = place_call(
        customer_number=body.customerNumber,
        assistant_id=body.assistantId or os.getenv("VAPI_ASSISTANT_OUTBOUND_ID") or os.getenv("VAPI_ASSISTANT_ID"),
        phone_number_id=body.phoneNumberId,
    )   # log immediately so you see it even before webhook arrives
    with SessionLocal() as db:
        db.add(CallLog(
            vapi_call_id=(data or {}).get("id"),
            direction="outbound",
            category="outbound",
            status="queued",
            patient_phone=body.customerNumber
       ))
    db.commit()
    return {"ok": True, "call": data}


@app.post("/scheduler/run_checkins_now")
def run_checkins_endpoint():
    run_checkins_now()
    return {"ok": True}
