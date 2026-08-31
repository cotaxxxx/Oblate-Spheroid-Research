import unittest
from producer.census_lower_edge_producer import produce_record
from checker.census_lower_edge_checker import verify

class CensusLowerEdgeTest(unittest.TestCase):
    def test_full_lambda_positive(self):
        record=produce_record()
        checked=verify(record)
        print("CENSUS_LOWER_EDGE producer pass:",record["gating_pass"])
        print("CENSUS_LOWER_EDGE checker enclosure:",checked)
        self.assertTrue(record["gating_pass"])

if __name__=="__main__": unittest.main()
