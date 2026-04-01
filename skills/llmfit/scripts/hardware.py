#!/usr/bin/env python3
"""
llmfit-hardware — Print hardware specs (alias for scan).
"""

import sys
from scan import main as scan_main

if __name__ == "__main__":
    sys.argv[0] = "llmfit-hardware"
    sys.exit(scan_main())
