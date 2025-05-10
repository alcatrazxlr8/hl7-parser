"""
Segment-specific parsers:
- parse_sch
- parse_pid
- parse_pv1
"""

from datetime import datetime
from typing import Optional

from datetime import datetime

def parse_sch(segment: str) -> dict:
	fields = segment.split("|")

	appointment_id = fields[1].split("^")[0] if len(fields) > 1 else None
	appointment_datetime_str = fields[11] if len(fields) > 11 else None
	appointment_datetime = (
		datetime.strptime(appointment_datetime_str, "%Y%m%d%H%M").isoformat() + "Z"
		if appointment_datetime_str
		else None
	)
	location = fields[20] if len(fields) > 20 and fields[20].strip() else None
	reason = fields[7] if len(fields) > 7 and fields[7].strip() else None

	return {
		"appointment_id": appointment_id,
		"appointment_datetime": appointment_datetime,
		"location": location,
		"reason": reason
	}

def parse_pid(segment: str) -> dict:
	fields = segment.split("|")

	id = fields[3].split("^")[0] if len(fields) > 3 else None

	name_parts = fields[5].split("^") if len(fields) > 5 else []
	first_name = name_parts[1] if len(name_parts) > 1 else None
	last_name = name_parts[0] if len(name_parts) > 0 else None
	middle_name = name_parts[2] if len(name_parts) > 2 else None

	dob = (
		datetime.strptime(fields[7], "%Y%m%d").date()
		if len(fields) > 7 and fields[7].strip()
		else None
	)
	gender = fields[8] if len(fields) > 8 else None

	return {
		"id": id,
		"first_name": first_name,
		"last_name": last_name,
		"middle_name": middle_name,
		"dob": dob,
		"gender": gender
	}

def parse_pv1(segment: str) -> dict:
	fields = segment.split("|")

	provider_field = fields[7] if len(fields) > 7 else None
	parts = provider_field.split("^")

	provider_id = parts[0] if len(parts) > 0 else None
	last_name = parts[1] if len(parts) > 1 else None
	prefix = parts[2] if len(parts) > 2 else None

	name = f"{prefix}. {last_name}" if prefix and last_name else last_name

	return {
		"id": provider_id,
		"name": name
	}
