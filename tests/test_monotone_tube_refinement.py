import unittest
from producer.monotone_tube_refinement_producer import produce_record
from checker.monotone_tube_refinement_checker import verify

class MonotoneTubeRefinementTest(unittest.TestCase):
    def test_refinement_full_64_box_negative(self):
        record=produce_record()
        unresolved=[r for r in record["parameter_boxes"] if not r["upper_negative"]]
        print("MONOTONE_TUBE_REFINEMENT unresolved producer boxes:",len(unresolved))
        for r in unresolved[:8]: print("UNRESOLVED",r)
        checked=verify(record)
        self.assertEqual(len(checked),64)
        self.assertTrue(record["gating_pass"])

if __name__=="__main__": unittest.main()
