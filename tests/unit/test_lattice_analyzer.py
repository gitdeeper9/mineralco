#!/usr/bin/env python3
"""
Unit tests for LatticeAnalyzer - Crystal symmetry and unit cell geometry
"""

import sys
import os
import unittest
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mineralco.engine.lattice_analyzer import LatticeAnalyzer, LatticeResult


class TestLatticeAnalyzer(unittest.TestCase):
    """Test suite for LatticeAnalyzer"""
    
    def test_cubic(self):
        """Test cubic crystal system (periclase)"""
        lattice = LatticeAnalyzer(a=4.2112, b=4.2112, c=4.2112, alpha=90, beta=90, gamma=90, z=4)
        self.assertEqual(lattice.crystal_system, "cubic")
        self.assertAlmostEqual(lattice.V0, 4.2112**3, places=3)
        
        # Test K' prior
        kprime_mean, kprime_std = lattice.get_kprime_prior()
        self.assertAlmostEqual(kprime_mean, 4.01, delta=0.1)
        
        print(f"\n📊 Periclase: V0={lattice.V0:.2f} Å³, V0_molar={lattice.V0_molar:.2f} cm³/mol")
    
    def test_orthorhombic(self):
        """Test orthorhombic crystal system (bridgmanite)"""
        lattice = LatticeAnalyzer(
            a=4.775, b=4.929, c=6.897, 
            alpha=90, beta=90, gamma=90,
            formula_weight=100.389, z=4
        )
        self.assertEqual(lattice.crystal_system, "orthorhombic")
        self.assertAlmostEqual(lattice.V0, 4.775 * 4.929 * 6.897, places=3)
        
        # V0_molar = V0 * 0.602214076 / z
        expected_V0_molar = lattice.V0 * 0.602214076 / 4
        self.assertAlmostEqual(lattice.V0_molar, expected_V0_molar, places=2)
        
        # Test density calculation
        self.assertIsNotNone(lattice.density)
        expected_density = lattice.formula_weight / lattice.V0_molar
        self.assertAlmostEqual(lattice.density, expected_density, places=2)
        
        print(f"\n📊 Bridgmanite:")
        print(f"  V0 = {lattice.V0:.2f} Å³")
        print(f"  V0_molar = {lattice.V0_molar:.2f} cm³/mol")
        print(f"  Density = {lattice.density:.2f} g/cm³")
        print(f"  Expected density ≈ 4.1 g/cm³")
    
    def test_monoclinic(self):
        """Test monoclinic crystal system (diopside)"""
        lattice = LatticeAnalyzer(
            a=9.746, b=8.899, c=5.251,
            alpha=90, beta=105.8, gamma=90,
            z=4
        )
        self.assertEqual(lattice.crystal_system, "monoclinic")
        
        # Test K' prior
        kprime_mean, kprime_std = lattice.get_kprime_prior()
        self.assertAlmostEqual(kprime_mean, 4.67, delta=0.1)
    
    def test_triclinic(self):
        """Test triclinic crystal system (kyanite)"""
        lattice = LatticeAnalyzer(
            a=7.126, b=7.852, c=5.572,
            alpha=89.9, beta=101.1, gamma=106.0,
            z=4
        )
        self.assertEqual(lattice.crystal_system, "triclinic")
        
        # Volume calculation for triclinic
        self.assertGreater(lattice.V0, 0)
        
        # Test K' prior
        kprime_mean, kprime_std = lattice.get_kprime_prior()
        self.assertAlmostEqual(kprime_mean, 4.91, delta=0.1)
    
    def test_tetragonal(self):
        """Test tetragonal crystal system (stishovite)"""
        lattice = LatticeAnalyzer(
            a=4.179, b=4.179, c=2.665,
            alpha=90, beta=90, gamma=90,
            z=2
        )
        self.assertEqual(lattice.crystal_system, "tetragonal")
    
    def test_hexagonal(self):
        """Test hexagonal crystal system (epsilon-iron)"""
        lattice = LatticeAnalyzer(
            a=2.470, b=2.470, c=3.950,
            alpha=90, beta=90, gamma=120,
            z=2
        )
        self.assertEqual(lattice.crystal_system, "hexagonal")
        
        # Hexagonal volume = (√3/2) * a² * c
        expected_V = (math.sqrt(3)/2) * 2.470**2 * 3.950
        self.assertAlmostEqual(lattice.V0, expected_V, places=2)
    
    def test_trigonal(self):
        """Test trigonal crystal system (corundum)"""
        lattice = LatticeAnalyzer(
            a=4.760, b=4.760, c=12.995,
            alpha=90, beta=90, gamma=120,
            z=6
        )
        # Corundum is trigonal but often classified as hexagonal
        self.assertIn(lattice.crystal_system, ["trigonal", "hexagonal"])
    
    def test_madelung_constant(self):
        """Test Madelung constant retrieval"""
        lattice = LatticeAnalyzer(a=4.2112, b=4.2112, c=4.2112)
        
        # NaCl structure
        m_nacl = lattice.get_madelung_constant("NaCl")
        self.assertAlmostEqual(m_nacl, 1.7476, places=3)
        
        # General cubic
        m_general = lattice.get_madelung_constant("general")
        self.assertAlmostEqual(m_general, 1.75, places=2)
    
    def test_born_lande_energy(self):
        """Test Born-Landé lattice energy calculation"""
        lattice = LatticeAnalyzer(
            a=4.2112, b=4.2112, c=4.2112,
            formula_weight=40.304, z=4
        )
        
        # MgO lattice energy (should be negative - attractive force)
        U = lattice.born_lande_energy(Z_plus=2, Z_minus=2, n=9)
        
        # Print for debugging
        print(f"\n📊 Born-Landé energy for MgO: {U:.1f} kJ/mol")
        
        # Lattice energy should be negative (attractive)
        self.assertLess(U, 0)
        # Magnitude should be several thousand kJ/mol
        self.assertGreater(abs(U), 3000)
        self.assertLess(abs(U), 5000)
    
    def test_summary(self):
        """Test summary dictionary"""
        lattice = LatticeAnalyzer(a=4.775, b=4.929, c=6.897, z=4)
        summary = lattice.summary()
        
        self.assertIn("crystal_system", summary)
        self.assertIn("V0_Ang3", summary)
        self.assertIn("V0_cm3_per_mol", summary)
        self.assertIn("kprime_prior_mean", summary)


if __name__ == '__main__':
    unittest.main()
