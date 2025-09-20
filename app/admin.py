from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Patient, Appointment, CallLog
import json

router = APIRouter(prefix="/admin", tags=["admin"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/patients")
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).order_by(Patient.id.desc()).all()

@router.get("/appointments")
def list_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).order_by(Appointment.id.desc()).all()

@router.get("/calls")
def list_calls(category: str | None = Query(None), db: Session = Depends(get_db)):
    q = db.query(CallLog).order_by(CallLog.id.desc())
    if category: q = q.filter(CallLog.category == category)
    rows = q.all()
    # parse structured JSON for convenience
    for r in rows:
        try: r.structured = json.loads(r.structured) if r.structured else None
        except Exception: pass
    return rows
