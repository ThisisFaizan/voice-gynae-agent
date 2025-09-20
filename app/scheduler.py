import os
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Patient, CallLog
from .vapi import place_call

scheduler = BackgroundScheduler()

def weekly_checkins():
    db: Session = SessionLocal()
    try:
        patients = db.query(Patient).filter(Patient.weekly_followup == True).all()
        patients = db.query(Patient).filter(Patient.weekly_followup == True).all()
        followup_assistant = os.getenv("VAPI_ASSISTANT_FOLLOWUP_ID") or os.getenv("VAPI_ASSISTANT_ID")
        for p in patients:
            try:
                print(f"[SCHED] calling {p.name} {p.phone}")
                place_call(customer_number=p.phone)
                db.add(CallLog(direction="outbound", patient_phone=p.phone))
                data = place_call(customer_number=p.phone, assistant_id=followup_assistant)
                db.add(CallLog(
                vapi_call_id=(data or {}).get("id"),
                direction="outbound",
                category="followup",
                status="queued",
                patient_phone=p.phone
            ))
                db.commit()
            except Exception as e:
                print("[SCHED][ERR]", p.phone, e)
    finally:
        db.close()

_started = False

def start_scheduler():
    global _started
    if _started:
        return
    scheduler.add_job(weekly_checkins, "cron", day_of_week="sun", hour=10, minute=0)  # Sunday 10:00
    scheduler.start()
    _started = True

def run_checkins_now():
    weekly_checkins()
    return True