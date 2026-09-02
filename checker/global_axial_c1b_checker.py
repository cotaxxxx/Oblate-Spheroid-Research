#!/usr/bin/env python3
"""Resumable C1b checker driver. Numerical work lives in the pinned lineage kernel."""
from checker import global_axial_c1b_kernel as kernel
from analysis.c1b_resumable_driver import main

if __name__ == "__main__":
    main(kernel, "checker")
