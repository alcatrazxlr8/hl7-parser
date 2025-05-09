import argparse
import json
from parser.hl7_parser import (
	read_hl7_file,
	message_parser,
	segment_parser,
	build_appointment_object
)

if __name__ == "__main__":
	filepath = "E:\Learn\hl7-parser\examples\example1.hl7"

	message = read_hl7_file(filepath)
	segments = message_parser(message)
	extracted = segment_parser(segments)

	try:
		appointment = build_appointment_object(extracted)
		print("✅ Parsed Appointment Object:")
		print(json.dumps(appointment, indent=2, default=str))  # default=str handles dates
	except ValueError as e:
		print(f"❌ Error: {e}")
