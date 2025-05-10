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
	build_appointment_object,
	split_messages
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

	input_base = os.path.splitext(os.path.basename(args.filepath))[0]

	try:
		## 1. Parse HL7
		message = read_hl7_file(args.filepath)
		messages = split_messages(message)

		appointments = []

		for index, raw_message in enumerate(messages, 1):
			segments = message_parser(raw_message)
			extracted = segment_parser(segments)
			appointment = build_appointment_object(extracted)
			# 2. Validate
			validated = Appointment(**appointment)
			appointments.append(validated)
			logging.info("Parsed message #%d successfully", index)

		logging.info("Validated appointment structure successfully.")

		## 2. Print to console
		# print("Parsed Appointment:")
		# print(validated.model_dump_json(indent=2 if args.pretty else None))
		print(f"\nParsed {len(appointments)} messages.")
		for i, appt in enumerate(appointments, 1):
			print(f"\nAppointment #{i}")
			print(appt.model_dump_json(indent=2 if args.pretty else None))

		## 3. Save parsed output to file
		# output_path = args.output or f"results/{input_base}.json"
		# output_dir = os.path.dirname(output_path)
		# if output_dir:
		# 	os.makedirs(output_dir, exist_ok=True)

		# with open(output_path, "w") as f:
		# 	f.write(validated.model_dump_json(indent=2))
		# print(f"Saved parsed appointment JSON to: {output_path}")
		# logging.info("Saved parsed appointment JSON to: %s", output_path)
		output_path = args.output or f"results/{input_base}.json"
		output_dir = os.path.dirname(output_path)
		if output_dir:
			os.makedirs(output_dir, exist_ok=True)

		with open(output_path, "w") as f:
			# json.dump([a.model_dump() for a in appointments], f, indent=2)
			f.write("[" + ",\n".join(a.model_dump_json(indent=2) for a in appointments) + "]")

		print(f"\nSaved parsed appointment(s) to: {output_path}")
		logging.info("Saved parsed appointment(s) to: %s", output_path)

		## 4. Export schema (accodring to cli flag)
		if args.export_schema:
			os.makedirs("schema", exist_ok=True)
			schema = Appointment.model_json_schema()
			schema_path = f"schema/{input_base}.schema.json"
			with open(schema_path, "w") as f:
				json.dump(schema, f, indent=2)
			logging.info("Exported JSON Schema to: %s", schema_path)
			print(f"Exported schema to: {schema_path}")


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
