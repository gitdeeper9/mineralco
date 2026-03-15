#!/usr/bin/env python3
"""
تشغيل جميع اختبارات MINERALCO
الاستخدام: python3 run_tests.py
"""

import unittest
import sys
import os

def main():
    """تشغيل جميع الاختبارات"""
    print("=" * 60)
    print("🧪 MINERALCO Test Runner")
    print("=" * 60)
    
    # إضافة المسار الرئيسي
    sys.path.insert(0, os.path.dirname(__file__))
    
    # اكتشاف جميع الاختبارات في مجلد tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # تشغيل الاختبارات
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # عرض الملخص
    print("\n" + "=" * 60)
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")
    print("=" * 60)
    
    return result

if __name__ == '__main__':
    main()
