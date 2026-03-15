#!/usr/bin/env python3
"""
Unit tests for EOSFitter - Birch-Murnaghan Equation of State
"""

import sys
import os
import unittest

# إضافة المسار الرئيسي
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mineralco.engine.eos_fitter import EOSFitter, EOSResult


class TestEOSFitter(unittest.TestCase):
    """Test suite for EOSFitter"""
    
    def setUp(self):
        """Prepare test data"""
        # Bridgmanite experimental data
        self.P_bridgmanite = [0.0, 5.2, 10.1, 15.3, 20.2, 25.4, 30.1, 35.0, 40.2, 45.1]
        self.V_bridgmanite = [24.45, 23.98, 23.52, 23.05, 22.61, 22.18, 21.78, 21.39, 21.02, 20.67]
        
        self.fitter = EOSFitter()
    
    def test_import(self):
        """Test that EOSFitter can be imported"""
        self.assertIsNotNone(EOSFitter)
    
    def test_fit_bridgmanite(self):
        """Test fitting bridgmanite data"""
        result = self.fitter.fit_simple(
            self.P_bridgmanite, 
            self.V_bridgmanite, 
            mineral="bridgmanite"
        )
        
        self.assertIsInstance(result, EOSResult)
        self.assertEqual(result.mineral, "bridgmanite")
        self.assertGreater(result.K0, 200)
        self.assertLess(result.K0, 300)
        
        print(f"\n✅ Bridgmanite: K₀={result.K0:.1f} GPa, RMS={result.rms_error:.3f}")
    
    def test_empty_data(self):
        """Test with empty data"""
        with self.assertRaises(Exception):
            self.fitter.fit_simple([], [])


if __name__ == '__main__':
    unittest.main()
