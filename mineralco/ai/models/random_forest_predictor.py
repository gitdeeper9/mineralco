#!/usr/bin/env python3
"""
MINERALCO-AI: Random Forest للتنبؤ بخصائص المعادن - نسخة مصححة
"""

import csv
import random
import math
import sys
from pathlib import Path
from collections import Counter

# إضافة المسار الرئيسي
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class DecisionTree:
    """شجرة قرار بسيطة"""
    
    def __init__(self, max_depth=5, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.tree = None
    
    def fit(self, X, y):
        """تدريب الشجرة"""
        self.tree = self._build_tree(X, y, depth=0)
    
    def _build_tree(self, X, y, depth):
        """بناء الشجرة بشكل متكرر"""
        n_samples = len(y)
        n_features = len(X[0]) if X else 0
        
        # شروط الإيقاف
        if (depth >= self.max_depth or 
            n_samples < self.min_samples_split or
            len(set(y)) == 1):
            return {'type': 'leaf', 'value': sum(y) / len(y) if y else 0}
        
        # البحث عن أفضل تقسيم
        best_feature, best_threshold, best_score = None, None, float('inf')
        
        for feature in range(n_features):
            values = [x[feature] for x in X]
            thresholds = sorted(set(values))
            
            for threshold in thresholds:
                left_X, left_y, right_X, right_y = self._split(X, y, feature, threshold)
                
                if not left_y or not right_y:
                    continue
                
                score = self._score_split(left_y, right_y)
                
                if score < best_score:
                    best_score = score
                    best_feature = feature
                    best_threshold = threshold
        
        if best_feature is None:
            return {'type': 'leaf', 'value': sum(y) / len(y) if y else 0}
        
        # تقسيم البيانات
        left_X, left_y, right_X, right_y = self._split(X, y, best_feature, best_threshold)
        
        # بناء الأشجار الفرعية
        left_tree = self._build_tree(left_X, left_y, depth + 1)
        right_tree = self._build_tree(right_X, right_y, depth + 1)
        
        return {
            'type': 'node',
            'feature': best_feature,
            'threshold': best_threshold,
            'left': left_tree,
            'right': right_tree
        }
    
    def _split(self, X, y, feature, threshold):
        """تقسيم البيانات"""
        left_X, left_y, right_X, right_y = [], [], [], []
        
        for i in range(len(X)):
            if X[i][feature] <= threshold:
                left_X.append(X[i])
                left_y.append(y[i])
            else:
                right_X.append(X[i])
                right_y.append(y[i])
        
        return left_X, left_y, right_X, right_y
    
    def _score_split(self, left_y, right_y):
        """حساب جودة التقسيم"""
        left_var = self._variance(left_y)
        right_var = self._variance(right_y)
        
        n_left = len(left_y)
        n_right = len(right_y)
        n_total = n_left + n_right
        
        return (n_left * left_var + n_right * right_var) / n_total
    
    def _variance(self, y):
        """حساب التباين"""
        if len(y) < 2:
            return 0
        mean = sum(y) / len(y)
        return sum((yi - mean) ** 2 for yi in y) / (len(y) - 1)
    
    def predict(self, X):
        """التنبؤ"""
        if not X:
            return []
        return [self._predict_row(x, self.tree) for x in X]
    
    def _predict_row(self, x, node):
        """التنبؤ لصف واحد"""
        if node['type'] == 'leaf':
            return node['value']
        
        if x[node['feature']] <= node['threshold']:
            return self._predict_row(x, node['left'])
        else:
            return self._predict_row(x, node['right'])


class RandomForestPredictor:
    """
    Random Forest للتنبؤ بخصائص المعادن
    
    يتنبأ بـ:
    - K0_out (bulk modulus)
    - Kprime_out (pressure derivative)
    - density_out
    - V0_out
    """
    
    def __init__(self, n_trees=10, max_depth=5):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.trees = []  # قائمة من القوائم: [ [trees_for_K0], [trees_for_Kprime], ... ]
        self.feature_names = []
        self.target_names = []
    
    def load_csv(self, filename):
        """تحميل البيانات من CSV"""
        X = []
        y_dict = {}
        
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            # تحديد targets (كل ما ينتهي بـ _out)
            self.target_names = [h for h in headers if h.endswith('_out')]
            self.feature_names = [h for h in headers if h not in self.target_names]
            
            # تهيئة y_dict
            for target in self.target_names:
                y_dict[target] = []
            
            for row in reader:
                if not row or len(row) < len(headers):
                    continue
                
                features = []
                for i, val in enumerate(row):
                    if headers[i] in self.feature_names:
                        try:
                            features.append(float(val))
                        except:
                            features.append(0.0)
                
                if features:
                    X.append(features)
                    
                    for target in self.target_names:
                        try:
                            idx = headers.index(target)
                            y_dict[target].append(float(row[idx]))
                        except (ValueError, IndexError):
                            y_dict[target].append(0.0)
        
        print(f"📊 Loaded {len(X)} samples")
        print(f"🔍 Features: {self.feature_names}")
        print(f"🎯 Targets: {self.target_names}")
        
        return X, y_dict
    
    def train(self, X, y_dict):
        """تدريب النماذج"""
        print(f"\n🌲 Training {self.n_trees} trees for each target...")
        self.trees = []
        
        for target_idx, target in enumerate(self.target_names):
            print(f"\n🎯 Target: {target}")
            y = y_dict[target]
            
            target_trees = []
            for i in range(self.n_trees):
                # Bootstrap sampling
                indices = [random.randint(0, len(X)-1) for _ in range(len(X))]
                X_sample = [X[i] for i in indices]
                y_sample = [y[i] for i in indices]
                
                # تدريب شجرة
                tree = DecisionTree(max_depth=self.max_depth)
                tree.fit(X_sample, y_sample)
                target_trees.append(tree)
                
                if (i + 1) % 5 == 0:
                    print(f"  Tree {i+1}/{self.n_trees} trained")
            
            self.trees.append(target_trees)
        
        print("\n✅ Training complete!")
    
    def predict(self, X):
        """التنبؤ لبيانات جديدة"""
        if not self.trees:
            print("⚠️ Model not trained yet!")
            return []
        
        predictions = []
        
        for target_idx, target_trees in enumerate(self.trees):
            target_preds = []
            for tree in target_trees:
                preds = tree.predict(X)
                target_preds.append(preds)
            
            # متوسط توقعات الأشجار
            avg_preds = []
            for i in range(len(X)):
                values = [tp[i] for tp in target_preds]
                avg_preds.append(sum(values) / len(values))
            
            predictions.append(avg_preds)
        
        # تجميع النتائج
        results = []
        for i in range(len(X)):
            result = {}
            for j, target in enumerate(self.target_names):
                result[target] = predictions[j][i]
            results.append(result)
        
        return results
    
    def predict_one(self, features):
        """التنبؤ لمعدن واحد"""
        results = self.predict([features])
        return results[0] if results else {}
    
    def evaluate(self, X_test, y_test_dict):
        """تقييم النموذج"""
        predictions = self.predict(X_test)
        
        print("\n📊 Evaluation Results:")
        print("-" * 40)
        
        for target in self.target_names:
            target_idx = self.target_names.index(target)
            actual = y_test_dict[target]
            predicted = [p[target] for p in predictions]
            
            # حساب RMSE
            errors = [(a - p) ** 2 for a, p in zip(actual, predicted)]
            rmse = math.sqrt(sum(errors) / len(errors)) if errors else 0
            
            # حساب R²
            mean_actual = sum(actual) / len(actual) if actual else 0
            ss_tot = sum((a - mean_actual) ** 2 for a in actual) if actual else 0
            ss_res = sum((a - p) ** 2 for a, p in zip(actual, predicted)) if actual else 0
            r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            print(f"\n🎯 {target}:")
            print(f"  RMSE: {rmse:.3f}")
            print(f"  R²:   {r2:.3f}")
        
        return predictions


def main():
    """اختبار النموذج"""
    print("="*50)
    print("🤖 MINERALCO-AI Random Forest Predictor")
    print("="*50)
    
    train_file = 'data/ai/training/train_data.csv'
    test_file = 'data/ai/training/test_data.csv'
    
    # تحقق من وجود الملفات
    if not Path(train_file).exists():
        print(f"❌ Training file not found: {train_file}")
        print("Please run data preparation first:")
        print("  python3 mineralco/ai/data/prepare_training_data.py")
        return
    
    # تحميل بيانات التدريب
    predictor = RandomForestPredictor(n_trees=10, max_depth=5)
    X_train, y_train = predictor.load_csv(train_file)
    
    # تحميل بيانات الاختبار
    X_test, y_test = predictor.load_csv(test_file)
    
    print(f"\n📊 Training samples: {len(X_train)}")
    print(f"📊 Test samples: {len(X_test)}")
    
    # تدريب النموذج
    predictor.train(X_train, y_train)
    
    # تقييم النموذج
    predictor.evaluate(X_test, y_test)


if __name__ == "__main__":
    main()
