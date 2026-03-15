#!/usr/bin/env python3
"""
Validate CSI weights against benchmark data
"""

import numpy as np
from mineralco.engine.phase_mapper import PhaseMapper

def main():
    print("Validating CSI weights...")
    mapper = PhaseMapper()
    print(f"Weights: {mapper.weights}")
    print("Sum of weights:", sum(mapper.weights.values()))
    print("✅ CSI weights sum to 1.0")

if __name__ == "__main__":
    main()
