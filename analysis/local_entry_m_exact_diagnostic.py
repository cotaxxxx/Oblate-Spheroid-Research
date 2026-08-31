#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY exact reconstruction of the local-entry uniform t-derivative margin."""
from producer.monotone_tube_refinement_producer import produce_record as produce_upper
from checker.monotone_tube_refinement_checker import verify as verify_upper
from producer.monotone_tube_lower_slab_producer import produce_record as produce_lower
from checker.monotone_tube_lower_slab_checker import verify as verify_lower


def main():
    upper = verify_upper(produce_upper())
    lower = verify_lower(produce_lower())
    upper_max = max(x.upper() for x in upper)
    lower_max = max(x.upper() for x in lower)
    all_max = max(upper_max, lower_max)
    m_exact = -all_max
    print("LOCAL_ENTRY_M_EXACT_DIAGNOSTIC — DIAGNOSTIC_ONLY / NOT_BINDING")
    print("UPPER_TUBE_MAX_UPPER_EXACT:", upper_max.str(100))
    print("LOWER_SLAB_MAX_UPPER_EXACT:", lower_max.str(100))
    print("GLOBAL_MAX_UPPER_EXACT:", all_max.str(100))
    print("M_EXACT:", m_exact.str(100))
    assert all_max < 0
    assert m_exact > 0


if __name__ == "__main__":
    main()
