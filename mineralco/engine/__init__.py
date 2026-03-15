"""
MINERALCO Engine Modules - نسخة مؤقتة (EOSFitter فقط)
"""

from mineralco.engine.eos_fitter import EOSFitter, EOSResult

# تم تعطيل المؤقت للوحدات الأخرى
# from mineralco.engine.thermal_corrector import ThermalCorrector, ThermalResult
# from mineralco.engine.lattice_analyzer import LatticeAnalyzer, LatticeResult
# from mineralco.engine.phase_mapper import PhaseMapper, CSIResult

__all__ = [
    'EOSFitter',
    'EOSResult',
    # 'ThermalCorrector',
    # 'ThermalResult',
    # 'LatticeAnalyzer',
    # 'LatticeResult',
    # 'PhaseMapper',
    # 'CSIResult',
]
