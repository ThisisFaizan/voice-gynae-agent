from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from datetime import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(32), unique=True, nullable=False)
    age = Column(Integer, nullable=True)
    pregnancy_status = Column(String(32), nullable=True)  # planning/pregnant/postpartum/unknown
    notes = Column(Text, nullable=True)
    weekly_followup = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    appointments = relationship("Appointment", back_populates="patient")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    when = Column(DateTime, nullable=False)
    reason = Column(String(200), nullable=True)
    admin_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient", back_populates="appointments")

class CallLog(Base):
    __tablename__ = "calls"
    id = Column(Integer, primary_key=True)
    vapi_call_id = Column(String(64), nullable=True)
    direction = Column(String(16))  # inbound/outbound
    patient_phone = Column(String(32), nullable=True)
    summary = Column(Text, nullable=True)
    transcript = Column(Text, nullable=True)
    structured = Column(Text, nullable=True)  # JSON string
    ended_reason = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String(16), nullable=True)  # inbound | outbound | followup
    status = Column(String(16), nullable=True)  # queued | completed | failed


