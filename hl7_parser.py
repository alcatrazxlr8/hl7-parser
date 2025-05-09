## CLI Entry point
"""
CLI entry point for HL7 SIU parser.
"""

import argparse
import json
from parser.hl7_parser import read_hl7_file, message_parser, segment_parser
from parser.segments import parse_sch  # More to be added later
