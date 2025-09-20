# app/webhook.py
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
import json
from .db import SessionLocal
from .models import CallLog

router = APIRouter(prefix="/vapi", tags=["vapi"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/webhook")
async def vapi_webhook(req: Request, db: Session = Depends(get_db)):
    body = await req.json()
    msg  = body.get("message", {})
    call_id = msg.get("id") or body.get("call", {}).get("id")
    ended_reason = (msg.get("endedReason") or "").strip()
    summary     = msg.get("summary")
    transcript  = msg.get("transcript")
    structured  = msg.get("structuredData") or msg.get("structured_data") or {}
    patient_phone = (structured.get("contact_number")
                     or structured.get("phone")
                     or structured.get("number"))

    structured_json = json.dumps(structured) if not isinstance(structured, str) else structured

    # upsert by vapi_call_id
    log = db.query(CallLog).filter(CallLog.vapi_call_id == call_id).first()
    if not log:
        log = CallLog(
            vapi_call_id=call_id,
            direction="inbound",
            category="inbound",
            patient_phone=patient_phone,
        )
        db.add(log)

    # update fields
    log.summary = summary
    log.transcript = transcript
    log.structured = structured_json
    log.ended_reason = ended_reason

    final = (ended_reason or "").lower()
    log.status = "completed" if final in ("completed", "endedbyassistant", "hangup") else "failed"

    db.commit()
    return {"ok": True}
