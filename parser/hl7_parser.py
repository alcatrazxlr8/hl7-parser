## core parsing logic
import re
from parser.segments import parse_sch, parse_pid, parse_pv1
# from segments import parse_pid, parse_pv1, parse_sch


# filepath = "E:\Learn\hl7-parser\examples\example1.hl7"

def read_hl7_file(filepath: str) -> str:
	"""
	Reads the content of an HL7 file and returns it as a raw string.
	"""
	with open(filepath, "r", encoding="utf-8") as file:
		message = file.read()
		return message


def message_parser(message) -> list[str]:

	segments = re.split(r'\r\n|\n|\r', message)
	segments = [seg for seg in segments if seg.strip()]

	return segments


## read each segment according to its use case
def segment_parser(segments):

	extracted_segments = {}

	for segment in segments:
		if segment.startswith("MSH") and "MSH" not in extracted_segments:
			extracted_segments["MSH"] = segment
		elif segment.startswith("SCH") and "SCH" not in extracted_segments:
			extracted_segments["SCH"] = segment
		elif segment.startswith("PID") and "PID" not in extracted_segments:
			extracted_segments["PID"] = segment
		elif segment.startswith("PV1") and "PV1" not in extracted_segments:
			extracted_segments["PV1"] = segment

	return extracted_segments


## combine parsed dicts into an appointment dict
def build_appointment_object(segments: dict) -> dict:
	sch_segment = segments.get("SCH")
	pid_segment = segments.get("PID")
	pv1_segment = segments.get("PV1")

	if not sch_segment:
		raise ValueError("Missing required SCH segment")
	if not pid_segment:
		raise ValueError("Missing required PID segment")
	if not pv1_segment:
		raise ValueError("Missing required PV1 segment")

	# Parse each segment
	sch_data = parse_sch(sch_segment)
	pid_data = parse_pid(pid_segment)
	pv1_data = parse_pv1(pv1_segment)

	# Build and return combined appointment object
	return {
		"appointment_id": sch_data["appointment_id"],
		"appointment_datetime": sch_data["appointment_datetime"],
		"location": sch_data["location"],
		"reason": sch_data["reason"],
		"patient": pid_data,
		"provider": pv1_data
	}

def split_messages(raw: str) -> list[str]:
	"""Splits a raw HL7 string into individual messages starting with MSH|"""
	chunks = re.split(r'(?=MSH\|)', raw)
	return [chunk.strip() for chunk in chunks if chunk.strip()]
