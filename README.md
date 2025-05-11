# HL7 SIU^S12 Parser

A Python based CLI tool for parsing HL7 SIU^S12 messages and converting them into structured JSON appointment records. Designed to be lightweight, readable, and extensible - without using external HL7 parsing libraries.

Supports single or multi-message HL7 files.

Outputs can be printed to console, saved to disk, and are validated using pydantic.

The JSON schema can also be generated as it is useful sometimes for OpenAPI docs etc.


## Features

- Parses HL7 SIU^S12 messages (segments: `MSH`, `SCH`, `PID`, `PV1`)
- Handles files with one or multiple messages
- Converts HL7 into structured JSON matching a Pydantic-defined schema
- CLI interface with optional output and schema export
- Schema validation built-in via Pydantic
- Logging of each run to `log.txt`
- Testing
- Docker support for easy containerized execution


### Example HL7 Message
```
MSH|^~\&|ADT1|GH HOSPITAL|GHH LAB, INC.|GH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|T|2.5.1
SCH|123456^A|...|...|...|...|...|General Consultation|...|...|...|202505021300|...|...|...|...|...|...|...|...|Clinic A - Room 203
PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A||19610615|M||2106-3|2222 HS^^City^NC^27401-1020
PV1|1|I|2000^2012^01||||D67890^Smith^Dr|||SUR||||7|A0|
```

### Output JSON format
This is what the output for the above HL7 message would look like
```json
{
  "appointment_id": "123456",
  "appointment_datetime": "2025-05-02T13:00:00Z",
  "location": "Clinic A - Room 203",
  "reason": "General Consultation",
  "patient": {
    "id": "PATID1234",
    "first_name": "ADAM",
    "last_name": "EVERYMAN",
    "middle_name": "A",
    "dob": "1961-06-15",
    "gender": "M"
  },
  "provider": {
    "id": "D67890",
    "name": "Dr. Smith"
  }
}
```

## Installation

### Option 1: Local Python environment

```bash
git clone https://github.com/alcatrazxlr8/hl7-parser.git
cd hl7-parser
python -m venv .venv
.venv\Scripts\activate   # "source venv/bin/activate" on Linux/Mac
pip install -r requirements.txt
```

### Option 2: Docker
```bash
docker build -t hl7-parser .
```

## CLI Usage

### Basic

```bash
python hl7_parser.py <path_to_hl7_file>
```

### Interactive
```bash
python hl7_parser.py
```
This prompts you to enter the path to the file at runtime through the terminal

NOTE: Interactive session doesn't work when running with docker

### Extra options

`--output <output_path>`    : Save the parsed JSON to a file (default: `results<input_name>.json`)

`--export-schema`           : Save the JSON schema to `schema/<input_name>.schema.json`

`--no-pretty`               Disable pretty-printing of JSON output

### Examples:

```bash
python hl7_parser.py examples/example1.hl7 --export-schema
```
- This uses the default output path for output files

<br>

```bash
python hl7_parser.py examples/example1.hl7 --output results/output.json --export-schema
```
## Docker Usage
We have to do the following and mount a volume because otherwise, even though the parser runs and a file is stored, the `--rm` flag means that any files thta are saved are ephemeral.

```bash
docker run --rm -v ${PWD}:/app hl7-parser <path_to_hl7_on_local_filesystem>
```
- we have to mention the input file path here
- all extra flags can be added here (`--output`, `--export-schema`)

## Multi-Message Support

If your HL7 file contains multiple messages separated by MSH|, each message is parsed and validated independently.
The CLI will:
- Print each parsed appointment to the terminal

- Save all results into a single JSON array (if `--output` is provided)

### Multi-message Output Format
Each HL7 message is converted into this JSON format:
```json
[{
  "appointment_id": "123456",
  "appointment_datetime": "2025-05-02T13:00:00Z",
  "location": "Clinic A - Room 203",
  "reason": "General Consultation",
  "patient": {
    "id": "P12345",
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "A",
    "dob": "1985-02-10",
    "gender": "M"
  },
  "provider": {
    "id": "D67890",
    "name": "Dr. Smith"
  }
},
{
  "appointment_id": "123456",
  "appointment_datetime": "2025-05-02T13:00:00Z",
  "location": "Clinic A - Room 203",
  "reason": "General Consultation",
  "patient": {
    "id": "PATID1234",
    "first_name": "ADAM",
    "last_name": "EVERYMAN",
    "middle_name": "A",
    "dob": "1961-06-15",
    "gender": "M"
  },
  "provider": {
    "id": "004777",
    "name": "AARON. ATTEND"
  }
}]
```
## Schema validation w/ Pydantic
Used Pydantic to define the structure of each parsed appointment and to enforce type validation.

By modeling the expected output using Pydantic's `BaseModel`, the parser ensures that every HL7 message is transformed into a clean, consistent, and validated JSON object. This approach also enables automatic schema generation and early error detection when fields are missing or improperly formatted.

Pydantic also provides better, more graceful handling of validation errors

## Testing
Tests are organized to cover:
- Segment-level parsing (SCH, PID, PV1)
- Full appointment building
- Validation edge cases

```bash
python -m unittest discover tests
```