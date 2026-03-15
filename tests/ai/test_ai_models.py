#!/usr/bin/env python3
"""
اختبارات الذكاء الاصطناعي لـ MINERALCO
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mineralco.ai.models.random_forest_predictor import RandomForestPredictor
from mineralco.ai.predictors.mineral_predictor import MineralAIPredictor


class TestAIModels(unittest.TestCase):
    """اختبار نماذج الذكاء الاصطناعي"""
    
    def test_random_forest_import(self):
        """اختبار استيراد RandomForest"""
        self.assertIsNotNone(RandomForestPredictor)
    
    def test_predictor_import(self):
        """اختبار استيراد MineralPredictor"""
        self.assertIsNotNone(MineralAIPredictor)
    
    def test_predictor_bridgmanite(self):
        """اختبار التنبؤ لبريدجمانيت"""
        predictor = MineralAIPredictor()
        result = predictor.predict_from_composition("MgSiO3", "orthorhombic")
        
        self.assertIn('K0_predicted', result)
        self.assertIn('Kprime_predicted', result)
        self.assertIn('density_predicted', result)
        
        # تحقق من قيم معقولة
        self.assertGreater(result['K0_predicted'], 200)
        self.assertLess(result['K0_predicted'], 300)
    
    def test_predictor_periclase(self):
        """اختبار التنبؤ لبيريكليس"""
        predictor = MineralAIPredictor()
        result = predictor.predict_from_composition("MgO", "cubic")
        
        self.assertGreater(result['K0_predicted'], 150)
        self.assertLess(result['K0_predicted'], 200)
    
    def test_phase_stability(self):
        """اختبار استقرار الطور"""
        predictor = MineralAIPredictor()
        result = predictor.predict_phase_stability(185, 39.49, 4.14, "cubic")
        
        self.assertIn('csi', result)
        self.assertIn('status', result)
        self.assertIn('stable', result)


if __name__ == '__main__':
    unittest.main()
