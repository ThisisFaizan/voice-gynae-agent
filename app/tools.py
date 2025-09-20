from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .db import SessionLocal
from .schemas import PatientUpsert, BookAppointment, NotifyDoctor
from .models import Patient, Appointment

router = APIRouter(prefix="/tools", tags=["tools"]) 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upsert_patient")
def upsert_patient(body: PatientUpsert, db: Session = Depends(get_db)):
    p = db.query(Patient).filter(Patient.phone == body.phone).first()
    if not p:
        p = Patient(phone=body.phone, name=body.name)
        db.add(p)
    p.age = body.age
    p.pregnancy_status = body.pregnancy_status
    p.weekly_followup = body.weekly_followup
    if body.notes:
        p.notes = (p.notes + "\n" if p.notes else "") + body.notes
    db.commit(); db.refresh(p)
    return {"ok": True, "patient_id": p.id}

@router.post("/book_appointment")
def book_appointment(body: BookAppointment, db: Session = Depends(get_db)):
    p = db.query(Patient).filter(Patient.phone == body.phone).first()
    if not p:
        p = Patient(phone=body.phone, name=body.phone)
        db.add(p); db.commit(); db.refresh(p)
    appt = Appointment(patient_id=p.id, when=body.when, reason=body.reason, admin_note=body.admin_note)
    db.add(appt); db.commit(); db.refresh(appt)
    return {"ok": True, "appointment_id": appt.id}

@router.post("/notify_doctor")
def notify_doctor(body: NotifyDoctor):
    print("[DOCTOR ALERT]", body.subject, "\n", body.summary, "\n", "phone:", body.phone or "-")
    return {"ok": True}
