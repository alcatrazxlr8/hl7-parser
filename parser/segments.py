"""
Segment-specific parsers:
- parse_sch
- parse_pid
- parse_pv1
"""

from datetime import datetime
from typing import Optional

def parse_sch(segment: str) -> dict:

	sch_fields = {"sch1": "appointment_id", "sch7": "appointment_datetime", "sch11": "location", "sch20": "reason"}
	fields = segment.split("|")

	sch_dict = {}
	sch_dict[sch_fields["sch1"]] = fields[1].split("^")[0]
	sch_dict[sch_fields["sch7"]] = datetime.strptime(fields[11], "%Y%m%d%H%M")
	sch_dict[sch_fields["sch11"]] = fields[11]
	sch_dict[sch_fields["sch20"]] = fields[20] | None
	return sch_dict