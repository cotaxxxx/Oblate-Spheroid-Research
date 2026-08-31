import unittest
from producer.census_lower_edge_refinement_producer import produce_record
from checker.census_lower_edge_refinement_checker import verify

class CensusLowerEdgeRefinementTest(unittest.TestCase):
    def test_refined_lambda_cover_positive(self):
        record=produce_record()
        checked=verify(record)
        weakest=min(checked,key=lambda item:item[2].lower())
        ll,lr,total=weakest
        print("CENSUS_LOWER_EDGE_REFINEMENT producer pass:",record["gating_pass"])
        print("CENSUS_LOWER_EDGE_REFINEMENT weakest lambda box:",str(ll),str(lr))
        print("CENSUS_LOWER_EDGE_REFINEMENT weakest mid:",total.mid().str(80))
        print("CENSUS_LOWER_EDGE_REFINEMENT weakest rad:",total.rad().str(80))
        print("CENSUS_LOWER_EDGE_REFINEMENT weakest lower:",total.lower().str(80))
        print("CENSUS_LOWER_EDGE_REFINEMENT weakest upper:",total.upper().str(80))
        self.assertTrue(record["gating_pass"])
        self.assertTrue(total.lower()>0)

if __name__=="__main__": unittest.main()
