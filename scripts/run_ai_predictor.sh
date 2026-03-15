#!/bin/bash
# تشغيل الذكاء الاصطناعي لـ MINERALCO - نسخة مصححة

echo "========================================="
echo "🤖 MINERALCO-AI Predictor"
echo "========================================="
echo ""

# إعداد بيانات التدريب
echo "📊 Step 1: Preparing training data..."
python3 mineralco/ai/data/prepare_training_data.py

echo ""
# تدريب النموذج
echo "🌲 Step 2: Training Random Forest model..."
python3 mineralco/ai/models/random_forest_predictor.py

echo ""
# اختبار الواجهة
echo "🧪 Step 3: Testing predictor interface..."
python3 mineralco/ai/predictors/mineral_predictor.py

echo ""
echo "========================================="
echo "✅ MINERALCO-AI setup complete!"
echo "========================================="
