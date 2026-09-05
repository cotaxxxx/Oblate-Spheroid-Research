import unittest
from producer.census_lower_edge_producer import produce_record
from checker.census_lower_edge_checker import verify

class CensusLowerEdgeTest(unittest.TestCase):
    def test_full_lambda_positive(self):
        record=produce_record()
        checked=verify(record)
        print("CENSUS_LOWER_EDGE producer pass:",record["gating_pass"])
        print("CENSUS_LOWER_EDGE producer mid:",record["total_mid"])
        print("CENSUS_LOWER_EDGE producer rad:",record["total_rad"])
        print("CENSUS_LOWER_EDGE checker mid:",checked.mid().str(80))
        print("CENSUS_LOWER_EDGE checker rad:",checked.rad().str(80))
        print("CENSUS_LOWER_EDGE checker lower:",checked.lower().str(80))
        print("CENSUS_LOWER_EDGE checker upper:",checked.upper().str(80))
        self.assertTrue(record["gating_pass"])
        self.assertTrue(checked.lower() > 0)

if __name__=="__main__": unittest.main()
