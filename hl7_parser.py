import os
import argparse
import json
import logging
from pydantic import ValidationError

from parser.models import Appointment
from parser.hl7_parser import (
	read_hl7_file,
	message_parser,
	segment_parser,
	build_appointment_object
)

logging.basicConfig(
	filename="log.txt",
	filemode="a",
	level=logging.INFO,
	format="%(asctime)s — %(levelname)s — %(message)s"
)


def main():
	parser = argparse.ArgumentParser(description="HL7 SIU^S12 Appointment Parser")
	parser.add_argument("filepath", help="Path to .hl7 file")
	parser.add_argument("--pretty", action="store_true", help="Pretty-print the JSON output")
	parser.add_argument("--output", help="Path to save parsed appointment JSON")
	parser.add_argument(
		"--export-schema",
		action="store_true",
		help="Export the JSON Schema for the Appointment model and exit"
	)

	args = parser.parse_args()
	logging.info("Started parsing HL7 file: %s", args.filepath)


	try:
		# 1. Parse HL7
		message = read_hl7_file(args.filepath)
		segments = message_parser(message)
		extracted = segment_parser(segments)
		appointment = build_appointment_object(extracted)

		# 2. Validate
		validated = Appointment(**appointment)
		logging.info("Validated appointment structure successfully.")

		# 3. Print to console
		print("Parsed Appointment:")
		print(validated.model_dump_json(indent=2 if args.pretty else None))

		# 4. Save parsed output to file
		if args.output:
			output_dir = os.path.dirname(args.output)
			if output_dir:
				os.makedirs(output_dir, exist_ok=True)

			with open(args.output, "w") as f:
				f.write(validated.model_dump_json(indent=2))
			print(f"Saved parsed appointment JSON to: {args.output}")
			logging.info("Saved parsed appointment JSON to: %s", args.output)

		# 5. Export schema (accodring to cli flag)
		if args.export_schema:
			os.makedirs("schema", exist_ok=True)
			schema = Appointment.model_json_schema()
			with open("schema/appointment_schema.json", "w") as f:
				json.dump(schema, f, indent=2)
			print("Exported schema to: schema/appointment_schema.json")
			logging.info("Exported JSON Schema to: schema/appointment_schema.json")

	except ValidationError as ve:
		# print("Validation failed:")
		# print(ve)  # Shows which field(s) failed
		for err in ve.errors():
			loc = ".".join(str(x) for x in err["loc"])
			print(f"	{loc}: {err['msg']} ({err['type']})")
			# logging.error("Validation failed: %s", ve)
			logging.error(f"	{loc}: {err['msg']} ({err['type']})")

	except Exception as e:
		print(f"Error: {e}")
		logging.error("Unexpected error: %s", e)

if __name__ == "__main__":
	main()
