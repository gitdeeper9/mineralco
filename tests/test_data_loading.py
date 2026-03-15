"""
Test data loading functionality
"""

import unittest
import json
import os
from pathlib import Path

class TestDataLoading(unittest.TestCase):
    
    def setUp(self):
        self.data_dir = Path("data")
    
    def test_cis_database_exists(self):
        """Test that CIS database file exists"""
        db_path = self.data_dir / "cis_database.json"
        self.assertTrue(db_path.exists(), "CIS database file not found")
    
    def test_cis_database_format(self):
        """Test CIS database format"""
        db_path = self.data_dir / "cis_database.json"
        with open(db_path, 'r') as f:
            data = json.load(f)
        
        self.assertIn("metadata", data)
        self.assertIn("minerals", data)
        self.assertGreater(len(data["minerals"]), 0, "No minerals found")
        
        # Check first mineral has required fields
        mineral = data["minerals"][0]
        required_fields = ["name", "formula", "crystal_system", "K0", "Kprime", "V0"]
        for field in required_fields:
            self.assertIn(field, mineral, f"Missing field: {field}")
    
    def test_pvt_benchmark_exists(self):
        """Test that P-V-T benchmark file exists"""
        pvt_path = self.data_dir / "pvt_benchmark.csv"
        self.assertTrue(pvt_path.exists(), "P-V-T benchmark file not found")
    
    def test_space_groups_exists(self):
        """Test that space groups file exists"""
        sg_path = self.data_dir / "space_groups.json"
        self.assertTrue(sg_path.exists(), "Space groups file not found")
    
    def test_prem_exists(self):
        """Test that PREM reference file exists"""
        prem_path = self.data_dir / "prem_reference.csv"
        self.assertTrue(prem_path.exists(), "PREM reference file not found")

if __name__ == '__main__':
    unittest.main()
