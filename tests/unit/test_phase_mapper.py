#!/usr/bin/env python3
"""
Unit tests for PhaseMapper - Crystal Stability Index
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mineralco.engine.phase_mapper import PhaseMapper, CSIResult


class TestPhaseMapper(unittest.TestCase):
    """Test suite for PhaseMapper"""
    
    def setUp(self):
        """Initialize PhaseMapper"""
        self.mapper = PhaseMapper()
    
    def test_import(self):
        """Test that PhaseMapper can be imported"""
        self.assertIsNotNone(PhaseMapper)
        self.assertIsNotNone(CSIResult)
    
    def test_default_weights(self):
        """Test default weights sum to 1"""
        weights = self.mapper.weights
        total = sum(weights.values())
        self.assertAlmostEqual(total, 1.0, places=5)
    
    def test_csi_cubic(self):
        """Test CSI for cubic mineral (ringwoodite near 660 km)"""
        result = self.mapper.compute_csi(
            K0=185.1,
            Vs=39.49,
            Kprime=4.14,
            Sy="cubic",
            alpha=2.10e-5,
            gamma=1.27
        )
        
        self.assertIsInstance(result, CSIResult)
        self.assertGreaterEqual(result.csi, 0)
        self.assertLessEqual(result.csi, 1)
        
        # Ringwoodite at 660 km should have high CSI
        print("\n" + "="*50)
        print("🔮 Ringwoodite CSI Test")
        print("="*50)
        print(f"CSI = {result.csi:.3f}")
        print(f"Status: {result.status}")
        print("="*50)
    
    def test_csi_orthorhombic(self):
        """Test CSI for orthorhombic mineral (bridgmanite)"""
        result = self.mapper.compute_csi(
            K0=260.7,
            Vs=24.45,
            Kprime=3.97,
            Sy="orthorhombic",
            alpha=2.00e-5,
            gamma=1.57
        )
        
        self.assertIsInstance(result, CSIResult)
        
        print("\n" + "="*50)
        print("🔮 Bridgmanite CSI Test")
        print("="*50)
        print(f"CSI = {result.csi:.3f}")
        print(f"Status: {result.status}")
        print("="*50)
    
    def test_symmetry_conversion(self):
        """Test symmetry to numeric conversion"""
        # Test different symmetry inputs
        self.assertEqual(self.mapper._symmetry_to_numeric("cubic"), 6.0)
        self.assertEqual(self.mapper._symmetry_to_numeric("tetragonal"), 5.0)
        self.assertEqual(self.mapper._symmetry_to_numeric("hexagonal"), 4.0)
        self.assertEqual(self.mapper._symmetry_to_numeric("trigonal"), 4.0)
        self.assertEqual(self.mapper._symmetry_to_numeric("orthorhombic"), 3.0)
        self.assertEqual(self.mapper._symmetry_to_numeric("monoclinic"), 2.0)
        self.assertEqual(self.mapper._symmetry_to_numeric("triclinic"), 1.0)
        
        # Test numeric input
        self.assertEqual(self.mapper._symmetry_to_numeric(5), 5.0)
    
    def test_csi_thresholds(self):
        """Test CSI threshold constants"""
        self.assertEqual(self.mapper.CSI_STABLE, 0.65)
        self.assertEqual(self.mapper.CSI_METASTABLE, 0.85)
        self.assertEqual(self.mapper.CSI_TRANSITION, 0.85)
    
    def test_csi_with_custom_weights(self):
        """Test CSI with custom weights"""
        custom_weights = {
            'K0': 0.3,
            'Vs': 0.2,
            'Kprime': 0.2,
            'Sy': 0.1,
            'alpha': 0.1,
            'gamma': 0.1
        }
        
        mapper = PhaseMapper(weights=custom_weights)
        total = sum(mapper.weights.values())
        self.assertAlmostEqual(total, 1.0, places=5)


if __name__ == '__main__':
    unittest.main()
