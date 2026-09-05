import unittest

from producer.gt_boundary_interval_producer import produce_record
from checker.gt_boundary_interval_checker import verify


class GTBoundaryIntervalTest(unittest.TestCase):
    def test_full_bracket_negative(self):
        record = produce_record(bits=160, panels=1024, degree=50)
        self.assertEqual(record["expectations"]["status"], "REPORTED_NOT_GATING")
        self.assertEqual(record["contract"]["required_sign"], "NEG")
        checked = verify(record)
        print("REPORTED checker enclosure:", checked)
        print("GATING criterion: upper endpoint < 0")
        self.assertLess(checked.upper(), 0)


if __name__ == "__main__":
    unittest.main()
