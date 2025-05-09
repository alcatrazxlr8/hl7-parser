## core parsing logic
import re

filepath = "E:\Learn\hl7-parser\examples\example1.hl7"

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
