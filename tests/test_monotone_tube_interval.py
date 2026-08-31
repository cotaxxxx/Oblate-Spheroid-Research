import unittest

from producer.monotone_tube_interval_producer import produce_record
from checker.monotone_tube_interval_checker import verify


class MonotoneTubeIntervalTest(unittest.TestCase):
    def test_full_fixed_tube_negative(self):
        record = produce_record()
        unresolved = [r for r in record["parameter_boxes"] if not r["upper_negative"]]
        print("MONOTONE_TUBE unresolved producer boxes:", len(unresolved))
        for r in unresolved:
            print("UNRESOLVED", r)
        self.assertTrue(record["gating_pass"])
        checked = verify(record)
        self.assertEqual(len(checked), 64)
        worst = max(x.upper() for x in checked)
        print("MONOTONE_TUBE worst checker upper endpoint:", worst)
        print("MONOTONE_TUBE parameter boxes:", len(checked))
        self.assertLess(worst, 0)


if __name__ == "__main__":
    unittest.main()
