"""
MINERALCO - نسخة مؤقتة للاختبار (EOSFitter فقط)
"""

__version__ = "1.0.0"
__author__ = "Samir Baladi"

# استيراد EOSFitter فقط (والباقي مؤقتاً)
from mineralco.engine.eos_fitter import EOSFitter, EOSResult

__all__ = [
    'EOSFitter',
    'EOSResult',
]

# Import AI modules
try:
    from mineralco.ai import MineralAIPredictor, RandomForestPredictor
    __all__.extend(['MineralAIPredictor', 'RandomForestPredictor'])
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    pass
