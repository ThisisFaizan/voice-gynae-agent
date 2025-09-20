from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime

class PatientUpsert(BaseModel):
    name: str
    phone: str
    age: Optional[int] = None
    pregnancy_status: Optional[str] = None
    weekly_followup: bool = False
    notes: Optional[str] = None

class BookAppointment(BaseModel):
    phone: str
    when: datetime
    reason: Optional[str] = None
    admin_note: Optional[str] = None

class NotifyDoctor(BaseModel):
    phone: Optional[str] = None
    subject: str
    summary: str

class OutboundRequest(BaseModel):
    customerNumber: str
    assistantId: Optional[str] = None
    phoneNumberId: Optional[str] = None

class VapiEvent(BaseModel):
    type: str
    message: Dict[str, Any] = Field(default_factory=dict)
