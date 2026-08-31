import unittest
from producer.census_lower_edge_refinement_producer import produce_record
from checker.census_lower_edge_refinement_checker import verify

class CensusLowerEdgeRefinementTest(unittest.TestCase):
    def test_refined_lambda_cover_positive(self):
        record=produce_record()
        weakest_rec=min(record["lambda_boxes"],key=lambda item: float(item["total_mid"].split()[0].strip("[]")) - float(item["total_rad"].split()[0].strip("[]")))
        print("CENSUS_LOWER_EDGE_REFINEMENT producer pass:",record["gating_pass"])
        print("CENSUS_LOWER_EDGE_REFINEMENT producer weakest lambda box:",weakest_rec["lambda_box"])
        print("CENSUS_LOWER_EDGE_REFINEMENT producer weakest mid:",weakest_rec["total_mid"])
        print("CENSUS_LOWER_EDGE_REFINEMENT producer weakest rad:",weakest_rec["total_rad"])
        checked=verify(record)
        weakest=min(checked,key=lambda item:item[2].lower())
        ll,lr,total=weakest
        print("CENSUS_LOWER_EDGE_REFINEMENT checker weakest lambda box:",str(ll),str(lr))
        print("CENSUS_LOWER_EDGE_REFINEMENT checker weakest mid:",total.mid().str(80))
        print("CENSUS_LOWER_EDGE_REFINEMENT checker weakest rad:",total.rad().str(80))
        print("CENSUS_LOWER_EDGE_REFINEMENT checker weakest lower:",total.lower().str(80))
        print("CENSUS_LOWER_EDGE_REFINEMENT checker weakest upper:",total.upper().str(80))
        self.assertTrue(record["gating_pass"])
        self.assertTrue(total.lower()>0)

if __name__=="__main__": unittest.main()
