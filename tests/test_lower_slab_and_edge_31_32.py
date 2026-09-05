import unittest
from producer.monotone_tube_lower_slab_producer import produce_record as produce_slab
from checker.monotone_tube_lower_slab_checker import verify as verify_slab
from producer.census_lower_edge_31_32_producer import produce_record as produce_edge
from checker.census_lower_edge_31_32_checker import verify as verify_edge

class LowerSlabAndEdgeTest(unittest.TestCase):
    def test_lower_slab_negative(self):
        r=produce_slab(); vals=verify_slab(r); worst=max(vals,key=lambda x:x.upper())
        print('LOWER_SLAB producer pass:',r['gating_pass'])
        print('LOWER_SLAB worst checker upper:',worst.upper().str(80))
        self.assertTrue(r['gating_pass'])
    def test_edge_31_32_positive(self):
        r=produce_edge(); vals=verify_edge(r); weakest=min(vals,key=lambda x:x[2].lower()); ll,lr,total=weakest
        print('EDGE_31_32 producer pass:',r['gating_pass'])
        print('EDGE_31_32 weakest lambda box:',str(ll),str(lr))
        print('EDGE_31_32 weakest mid:',total.mid().str(80))
        print('EDGE_31_32 weakest rad:',total.rad().str(80))
        print('EDGE_31_32 weakest lower:',total.lower().str(80))
        print('EDGE_31_32 weakest upper:',total.upper().str(80))
        self.assertTrue(r['gating_pass'])

if __name__=='__main__': unittest.main()
