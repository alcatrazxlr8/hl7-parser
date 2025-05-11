import unittest
from parser.hl7_parser import build_appointment_object
from parser.models import Appointment
from datetime import date

class TestBuildAppointmentObject(unittest.TestCase):
	def test_valid_segments_builds_correct_appointment(self):
		segments = {
			"SCH": "SCH|123456^A|...|...|...|...|...|General Consultation|...|...|...|202505021300|...|...|...|...|...|...|...|...|Clinic A - Room 203",
			"PID": "PID|1||P12345^^^HOSP^MR||Doe^John^A||19850210|M",
			"PV1": "PV1|1|...|...|...|...|...|D67890^Smith^Dr"
		}

		result = build_appointment_object(segments)

		# Validate basic keys
		self.assertEqual(result["appointment_id"], "123456")
		self.assertEqual(result["location"], "Clinic A - Room 203")
		self.assertEqual(result["reason"], "General Consultation")
		self.assertEqual(result["patient"]["first_name"], "John")
		self.assertEqual(result["provider"]["name"], "Dr. Smith")

		# Pass to Pydantic for confirmation
		validated = Appointment(**result)
		self.assertEqual(validated.patient.dob, date(1985, 2, 10))

	def test_missing_pid_segment_raises_error(self):
		segments = {
			"SCH": "SCH|123456^A|...|...|...|...|...|Checkup|...|...|...|202505021300|...|...|...|...|...|...|...|...|Clinic A",
			# PID is missing
			"PV1": "PV1|1|...|...|...|...|...|D123^Somebody^Dr"
		}

		with self.assertRaises(ValueError) as ctx:
			build_appointment_object(segments)
		self.assertIn("PID", str(ctx.exception))
