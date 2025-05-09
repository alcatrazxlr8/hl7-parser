import argparse
import json
from parser.hl7_parser import (
	read_hl7_file,
	message_parser,
	segment_parser,
	build_appointment_object
)

def main():
	parser = argparse.ArgumentParser(description="HL7 SIU^S12 Appointment Parser")
	parser.add_argument("filepath", help="Path to .hl7 file")
	parser.add_argument("--pretty", action="store_true", help="Pretty-print the JSON output")
	
	args = parser.parse_args()

	try:
		message = read_hl7_file(args.filepath)
		segments = message_parser(message)
		extracted = segment_parser(segments)
		appointment = build_appointment_object(extracted)

		if args.pretty:
			print(json.dumps(appointment, indent=2, default=str))
		else:
			print(json.dumps(appointment, default=str))

	except Exception as e:
		print(f"Error: {e}")

if __name__ == "__main__":
	main()
