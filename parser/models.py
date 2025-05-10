from pydantic import BaseModel
from typing import Optional
from datetime import date

class Patient(BaseModel):
	id: str
	first_name: str
	last_name: str
	middle_name: Optional[str] = None
	dob: date
	gender: Optional[str] = None

class Provider(BaseModel):
	id: str
	name: str

class Appointment(BaseModel):
	appointment_id: str
	appointment_datetime: str  # already ISO-formatted string so keeping it as "str"
	location: Optional[str] = None
	reason: Optional[str] = None
	patient: Patient
	provider: Provider
