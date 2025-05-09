import unittest
from datetime import datetime, date
from parser.segments import parse_sch, parse_pid, parse_pv1

class TestParseSCH(unittest.TestCase):
	def test_basic_sch_parsing(self):
		segment = "SCH|123456^A|...|...|...|...|...|General Consultation|...|...|...|202505021300|...|...|...|...|...|...|...|...|Clinic A - Room 203"
		result = parse_sch(segment)

		self.assertEqual(result["appointment_id"], "123456")
		self.assertEqual(result["appointment_datetime"], "2025-05-02T13:00:00Z")
		self.assertEqual(result["location"], "Clinic A - Room 203")
		self.assertEqual(result["reason"], "General Consultation")

class TestParsePID(unittest.TestCase):
	def test_basic_pid_parsing(self):
		segment = "PID|1||P12345^^^HOSP^MR||Doe^John^A||19850210|M"
		result = parse_pid(segment)

		self.assertEqual(result["id"], "P12345")
		self.assertEqual(result["first_name"], "John")
		self.assertEqual(result["last_name"], "Doe")
		self.assertEqual(result["middle_name"], "A")
		self.assertEqual(result["dob"], date(1985, 2, 10))
		self.assertEqual(result["gender"], "M")

class TestParsePV1(unittest.TestCase):
	def test_basic_pv1_parsing(self):
		segment = "PV1|1|...|...|...|...|...|D67890^Smith^Dr"
		result = parse_pv1(segment)

		self.assertEqual(result["id"], "D67890")
		self.assertEqual(result["name"], "Dr. Smith")
