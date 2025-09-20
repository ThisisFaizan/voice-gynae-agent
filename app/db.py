import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Patient, Appointment, CallLog

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gynae.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    Base.metadata.create_all(bind=engine)

# Convenience helpers
def get_or_create_patient(db, phone: str, name: str | None = None):
    p = db.query(Patient).filter(Patient.phone == phone).first()
    if p:
        return p
    p = Patient(phone=phone, name=name or phone)
    db.add(p)
    db.commit(); db.refresh(p)
    return p
