"""
Test data directory organization
"""

import unittest
import json
from pathlib import Path

class TestDataOrganization(unittest.TestCase):
    
    def setUp(self):
        self.data_dir = Path("data")
    
    def test_directory_structure(self):
        """Test that all required directories exist"""
        required_dirs = [
            "databases/cis",
            "databases/space_groups",
            "experimental/dac",
            "reference/prem",
            "sample/tutorials",
        ]
        
        for dir_path in required_dirs:
            full_path = self.data_dir / dir_path
            self.assertTrue(full_path.exists(), f"Directory missing: {dir_path}")
            self.assertTrue(full_path.is_dir(), f"Not a directory: {dir_path}")
    
    def test_cis_database_location(self):
        """Test CIS database is in correct location"""
        db_path = self.data_dir / "databases/cis/cis_database_v1.0.0.json"
        self.assertTrue(db_path.exists(), "CIS database not in correct location")
    
    def test_space_groups_location(self):
        """Test space groups database is in correct location"""
        sg_path = self.data_dir / "databases/space_groups/space_groups_230.json"
        self.assertTrue(sg_path.exists(), "Space groups not in correct location")
    
    def test_prem_location(self):
        """Test PREM reference is in correct location"""
        prem_path = self.data_dir / "reference/prem/prem_1981_updated.csv"
        self.assertTrue(prem_path.exists(), "PREM not in correct location")
    
    def test_experimental_data_location(self):
        """Test experimental data is in correct location"""
        exp_path = self.data_dir / "experimental/dac/combined_dac_data.csv"
        self.assertTrue(exp_path.exists(), "Experimental data not in correct location")
    
    def test_data_index(self):
        """Test data index file exists and is valid"""
        index_path = self.data_dir / "data_index.json"
        self.assertTrue(index_path.exists(), "Data index not found")
        
        with open(index_path, 'r') as f:
            index = json.load(f)
        
        self.assertIn("metadata", index)
        self.assertIn("databases", index)
        self.assertIn("experimental", index)
        self.assertIn("reference", index)

if __name__ == '__main__':
    unittest.main()
