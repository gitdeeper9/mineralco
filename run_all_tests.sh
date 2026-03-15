#!/bin/bash
echo "========================================"
echo "🧪 تشغيل جميع اختبارات MINERALCO"
echo "========================================"

echo -e "\n📦 اختبارات الوحدة (Unit Tests):"
python3 -m unittest discover -s tests/unit -v

echo -e "\n🔗 اختبارات التكامل (Integration Tests):"
python3 -m unittest discover -s tests/integration -v

echo -e "\n✅ اختبارات التحقق (Validation Tests):"
python3 -m unittest discover -s tests/validation -v

echo -e "\n📊 اختبارات البيانات (Data Tests):"
python3 -m unittest tests.test_data_loading tests.test_data_organization -v

echo -e "\n========================================"
echo "✅ جميع الاختبارات اكتملت"
echo "========================================"
