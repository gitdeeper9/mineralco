#!/usr/bin/env python3
"""
Unit tests for ThermalCorrector - Mie-Grüneisen thermal pressure correction
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mineralco.engine.thermal_corrector import ThermalCorrector, ThermalResult


class TestThermalCorrector(unittest.TestCase):
    """Test suite for ThermalCorrector"""
    
    def setUp(self):
        """Initialize with bridgmanite parameters"""
        self.tc = ThermalCorrector(
            K0=260.7,
            Kprime=3.97,
            V0=24.45,
            gamma0=1.57,
            alpha0=2.0e-5,
            n_atoms=5
        )
    
    def test_import(self):
        """Test that ThermalCorrector can be imported"""
        self.assertIsNotNone(ThermalCorrector)
        self.assertIsNotNone(ThermalResult)
    
    def test_initialization(self):
        """Test initialization with bridgmanite parameters"""
        self.assertAlmostEqual(self.tc.K0, 260.7)
        self.assertAlmostEqual(self.tc.Kprime, 3.97)
        self.assertAlmostEqual(self.tc.V0, 24.45)
        self.assertAlmostEqual(self.tc.gamma0, 1.57)
        self.assertGreater(self.tc.theta_D0, 500)  # Should be > 500 K
    
    def test_gamma_volume_dependence(self):
        """Test volume-dependent Grüneisen parameter"""
        # At V0, gamma should equal gamma0
        self.assertAlmostEqual(self.tc.gamma(self.tc.V0), self.tc.gamma0)
        
        # At smaller volume, gamma should be larger (since q > 0)
        V_small = self.tc.V0 * 0.8
        self.assertGreater(self.tc.gamma(V_small), self.tc.gamma0)
        
        # At larger volume, gamma should be smaller
        V_large = self.tc.V0 * 1.2
        self.assertLess(self.tc.gamma(V_large), self.tc.gamma0)
    
    def test_thermal_energy(self):
        """Test thermal energy calculation"""
        # At reference temperature, thermal energy should be lower
        E_300 = self.tc.thermal_energy(self.tc.V0, 300)
        E_1000 = self.tc.thermal_energy(self.tc.V0, 1000)
        E_2000 = self.tc.thermal_energy(self.tc.V0, 2000)
        
        self.assertGreater(E_2000, E_1000)
        self.assertGreater(E_1000, E_300)
        self.assertGreater(E_300, 0)
    
    def test_thermal_pressure(self):
        """Test thermal pressure calculation"""
        # At reference temperature, thermal pressure should be near zero
        P_th_300 = self.tc.thermal_pressure(self.tc.V0, 300)
        self.assertAlmostEqual(P_th_300, 0, places=1)
        
        # At higher temperature, thermal pressure should be positive
        P_th_2000 = self.tc.thermal_pressure(self.tc.V0, 2000)
        self.assertGreater(P_th_2000, 0)
        
        # Thermal pressure should increase with temperature
        P_th_1000 = self.tc.thermal_pressure(self.tc.V0, 1000)
        self.assertGreater(P_th_2000, P_th_1000)
        
        print(f"\n📊 Thermal pressure at V0:")
        print(f"  T=300K:  {P_th_300:.3f} GPa")
        print(f"  T=1000K: {P_th_1000:.3f} GPa")
        print(f"  T=2000K: {P_th_2000:.3f} GPa")
    
    def test_total_pressure(self):
        """Test total pressure calculation"""
        V = 20.0  # Compressed volume
        
        result_300 = self.tc.pressure(V, 300)
        result_2000 = self.tc.pressure(V, 2000)
        
        self.assertIsInstance(result_300, ThermalResult)
        self.assertIsInstance(result_2000, ThermalResult)
        
        # Total pressure should be higher at higher temperature
        self.assertGreater(result_2000.P_total, result_300.P_total)
        
        print(f"\n📊 Total pressure at V={V:.1f} cm³/mol:")
        print(f"  T=300K:  P_total={result_300.P_total:.1f} GPa")
        print(f"  T=2000K: P_total={result_2000.P_total:.1f} GPa")
        print(f"  Thermal contribution: {result_2000.P_thermal:.2f} GPa")
    
    def test_volume_at_PT(self):
        """Test volume solving at given P and T"""
        # Find volume at 50 GPa, 2000 K
        V = self.tc.volume_at_PT(P_target=50, T=2000)
        
        self.assertGreater(V, 0)
        self.assertLess(V, self.tc.V0)  # Should be compressed
        
        # Verify the solution
        result = self.tc.pressure(V, 2000)
        self.assertAlmostEqual(result.P_total, 50, delta=1.0)
        
        print(f"\n📊 Volume at P=50 GPa, T=2000 K: {V:.2f} cm³/mol")
        print(f"  Verified P={result.P_total:.1f} GPa")
    
    def test_murnaghan_approximation(self):
        """Test Murnaghan isothermal pressure approximation"""
        V = 20.0
        result = self.tc.pressure(V, 300)
        
        # At 300K, thermal pressure is small, so P_total should be close to P_iso
        self.assertAlmostEqual(result.P_total, result.P_thermal + 
                              (self.tc.K0/self.tc.Kprime) * ((self.tc.V0/V) ** self.tc.Kprime - 1),
                              delta=0.1)


if __name__ == '__main__':
    unittest.main()
