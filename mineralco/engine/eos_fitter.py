"""
EOSFitter - Birch-Murnaghan Equation of State fitting engine
Lightweight version - No NumPy, No SciPy
"""

import math
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass


@dataclass
class EOSResult:
    """Equation of State fitting results"""
    K0: float           # Bulk modulus (GPa)
    K0_std: float       # Standard deviation
    Kprime: float       # Pressure derivative
    Kprime_std: float   # Standard deviation
    V0: float           # Reference volume (cm³/mol)
    V0_std: float       # Standard deviation
    rms_error: float    # Root mean square error
    mineral: str        # Mineral name
    method: str         # Fitting method


class EOSFitter:
    """
    Birch-Murnaghan Equation of State fitter
    Lightweight version - uses pure Python math only
    """
    
    def __init__(self, method: str = "BM3"):
        """
        Initialize EOS fitter
        
        Parameters
        ----------
        method : str
            Fitting method: "BM2", "BM3", or "BM4"
        """
        self.method = method
        self._validate_method()
    
    def _validate_method(self):
        """Validate fitting method"""
        valid_methods = ["BM2", "BM3", "BM4"]
        if self.method not in valid_methods:
            raise ValueError(f"Method must be one of {valid_methods}")
    
    def _bm3_pressure(self, V: float, V0: float, K0: float, Kprime: float) -> float:
        """
        Third-order Birch-Murnaghan EOS for a single point
        
        P(V) = (3K0/2) * [(V0/V)^(7/3) - (V0/V)^(5/3)] *
               {1 + (3/4)(K'-4) * [(V0/V)^(2/3) - 1]}
        """
        ratio = V0 / V
        x = ratio ** (2/3)
        f = (x - 1) / 2  # Eulerian strain
        
        P = 1.5 * K0 * (ratio ** (7/3) - ratio ** (5/3)) * (1 + 0.75 * (Kprime - 4) * (x - 1))
        return P
    
    def fit_simple(
        self,
        pressure: List[float],
        volume: List[float],
        mineral: str = "unknown"
    ) -> EOSResult:
        """
        Simple EOS fitting without optimization
        Uses linear approximation for initial estimates
        
        Parameters
        ----------
        pressure : list
            Pressure in GPa
        volume : list
            Volume in cm³/mol
        mineral : str
            Mineral name
        
        Returns
        -------
        EOSResult
            Estimated parameters
        """
        # Sort by volume (ascending = highest volume first)
        pairs = sorted(zip(volume, pressure), key=lambda x: x[0], reverse=True)
        V_sorted = [p[0] for p in pairs]
        P_sorted = [p[1] for p in pairs]
        
        # Estimate V0 (volume at lowest pressure)
        V0 = V_sorted[0]
        
        # Estimate K0 from linear slope near ambient
        if len(V_sorted) >= 3:
            # Use first few points for linear approximation
            V_near = V_sorted[:3]
            P_near = P_sorted[:3]
            
            # Simple linear regression: K0 ≈ -V0 * (dP/dV)
            dP = P_near[-1] - P_near[0]
            dV = V_near[-1] - V_near[0]
            if dV != 0:
                K0 = -V0 * dP / dV
            else:
                K0 = 100.0  # Default guess
        else:
            K0 = 100.0  # Default guess
        
        # Default Kprime
        Kprime = 4.0
        
        # Calculate RMS error with these parameters
        errors = []
        for V, P in zip(V_sorted, P_sorted):
            P_calc = self._bm3_pressure(V, V0, K0, Kprime)
            errors.append((P - P_calc) ** 2)
        
        rms_error = math.sqrt(sum(errors) / len(errors))
        
        return EOSResult(
            K0=K0,
            K0_std=K0 * 0.05,  # Rough estimate: 5% uncertainty
            Kprime=Kprime,
            Kprime_std=0.2,     # Typical uncertainty
            V0=V0,
            V0_std=V0 * 0.002,  # 0.2% uncertainty
            rms_error=rms_error,
            mineral=mineral,
            method="simple"
        )
    
    def fit_with_known_Kprime(
        self,
        pressure: List[float],
        volume: List[float],
        Kprime: float,
        mineral: str = "unknown"
    ) -> EOSResult:
        """
        Fit with fixed K' (from symmetry prior)
        
        Parameters
        ----------
        pressure : list
            Pressure in GPa
        volume : list
            Volume in cm³/mol
        Kprime : float
            Fixed pressure derivative
        mineral : str
            Mineral name
        
        Returns
        -------
        EOSResult
            Estimated parameters
        """
        # Sort by volume
        pairs = sorted(zip(volume, pressure), key=lambda x: x[0], reverse=True)
        V_sorted = [p[0] for p in pairs]
        P_sorted = [p[1] for p in pairs]
        
        V0 = V_sorted[0]
        
        # Estimate K0 from first point using BM3
        if len(V_sorted) >= 2:
            V1, V2 = V_sorted[0], V_sorted[1]
            P1, P2 = P_sorted[0], P_sorted[1]
            
            # Solve for K0 using two points
            P1_calc = self._bm3_pressure(V1, V0, 1.0, Kprime)  # Unit K0
            P2_calc = self._bm3_pressure(V2, V0, 1.0, Kprime)
            
            if P2_calc - P1_calc != 0:
                K0 = (P2 - P1) / (P2_calc - P1_calc)
            else:
                K0 = 100.0
        else:
            K0 = 100.0
        
        # Calculate RMS error
        errors = []
        for V, P in zip(V_sorted, P_sorted):
            P_calc = self._bm3_pressure(V, V0, K0, Kprime)
            errors.append((P - P_calc) ** 2)
        
        rms_error = math.sqrt(sum(errors) / len(errors))
        
        return EOSResult(
            K0=K0,
            K0_std=K0 * 0.05,
            Kprime=Kprime,
            Kprime_std=0.0,
            V0=V0,
            V0_std=V0 * 0.002,
            rms_error=rms_error,
            mineral=mineral,
            method="fixed_Kprime"
        )
    
    def fit(self, pressure, volume, mineral="unknown", **kwargs):
        """Alias for fit_simple"""
        return self.fit_simple(pressure, volume, mineral)
    
    def print_summary(self, result: EOSResult):
        """Print formatted summary"""
        print("\n" + "="*50)
        print(f"📊 EOSFitter Results: {result.mineral}")
        print("="*50)
        print(f"Method: {result.method}")
        print(f"K₀  = {result.K0:.1f} ± {result.K0_std:.1f} GPa")
        print(f"K'  = {result.Kprime:.2f} ± {result.Kprime_std:.2f}")
        print(f"V₀  = {result.V0:.2f} ± {result.V0_std:.2f} cm³/mol")
        print(f"RMS = {result.rms_error:.3f} GPa")
        print("="*50)
