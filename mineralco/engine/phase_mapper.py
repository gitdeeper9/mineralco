"""
PhaseMapper - Crystal Stability Index and phase boundary prediction
Lightweight version - No NumPy
"""

import math
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass


@dataclass
class CSIResult:
    """Crystal Stability Index results"""
    csi: float
    status: str  # "STABLE", "METASTABLE", "TRANSITION IMMINENT"
    normalized_params: Dict[str, float]
    weights: Dict[str, float]


class PhaseMapper:
    """
    Crystal Stability Index (CSI) computation and phase boundary prediction
    
    CSI = w₁·K₀* + w₂·V_s* + w₃·K'* + w₄·S_y* + w₅·α* + w₆·γ* + w₇·Φ_latt*
    
    Default weights (from PCA-regularized regression):
    w₁=0.28, w₂=0.19, w₃=0.17, w₄=0.13, w₅=0.10, w₆=0.09, w₇=0.04
    """
    
    # Default CSI weights (from paper)
    DEFAULT_WEIGHTS = {
        'K0': 0.28,
        'Vs': 0.19,
        'Kprime': 0.17,
        'Sy': 0.13,
        'alpha': 0.10,
        'gamma': 0.09,
        'U_lattice': 0.04
    }
    
    # Critical thresholds
    CSI_STABLE = 0.65
    CSI_METASTABLE = 0.85
    CSI_TRANSITION = 0.85
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Initialize PhaseMapper
        
        Parameters
        ----------
        weights : dict, optional
            Custom weights for CSI calculation
            If None, uses DEFAULT_WEIGHTS
        """
        self.weights = weights if weights else self.DEFAULT_WEIGHTS.copy()
        
        # Validate weights sum to 1.0
        total = sum(self.weights.values())
        if abs(total - 1.0) > 1e-6:
            # Normalize
            for key in self.weights:
                self.weights[key] /= total
    
    def _normalize_parameter(
        self,
        param_name: str,
        value: float,
        mineral: Optional[str] = None
    ) -> float:
        """
        Normalize parameter to [0,1] range
        
        For general use without specific mineral, uses global ranges
        """
        # Global normalization ranges based on 47-mineral benchmark
        ranges = {
            'K0': (50, 350),      # GPa
            'Vs': (5, 150),       # cm³/mol
            'Kprime': (3, 8),      # dimensionless
            'Sy': (0, 6),          # symmetry order (cubic=6, triclinic=0)
            'alpha': (1e-5, 4e-5), # K⁻¹
            'gamma': (0.8, 2.0),   # dimensionless
            'U_lattice': (5000, 25000)  # kJ/mol
        }
        
        if param_name not in ranges:
            return 0.5  # Default if unknown
        
        min_val, max_val = ranges[param_name]
        norm = (value - min_val) / (max_val - min_val)
        
        # Clamp to [0, 1]
        if norm < 0:
            norm = 0
        if norm > 1:
            norm = 1
            
        return norm
    
    def _symmetry_to_numeric(self, symmetry: Union[str, int]) -> float:
        """
        Convert crystal symmetry to numeric value for normalization
        
        Order: cubic (6) > tetragonal (5) > hexagonal (4) > 
               orthorhombic (3) > monoclinic (2) > triclinic (1)
        """
        if isinstance(symmetry, (int, float)):
            return float(symmetry)
        
        sym_map = {
            "cubic": 6.0,
            "tetragonal": 5.0,
            "hexagonal": 4.0,
            "trigonal": 4.0,
            "orthorhombic": 3.0,
            "monoclinic": 2.0,
            "triclinic": 1.0
        }
        
        return sym_map.get(symmetry.lower(), 3.0)
    
    def compute_csi(
        self,
        K0: float,
        Vs: float,
        Kprime: float,
        Sy: Union[str, int],
        alpha: float,
        gamma: float,
        U_lattice: Optional[float] = None,
        mineral: Optional[str] = None
    ) -> CSIResult:
        """
        Compute Crystal Stability Index
        
        Parameters
        ----------
        K0 : float
            Bulk modulus (GPa)
        Vs : float
            Specific volume (cm³/mol)
        Kprime : float
            Pressure derivative
        Sy : str or int
            Crystal symmetry (system name or numeric value)
        alpha : float
            Thermal expansion coefficient (K⁻¹)
        gamma : float
            Grüneisen parameter
        U_lattice : float, optional
            Lattice energy (kJ/mol)
        mineral : str, optional
            Mineral name for specific normalization
            
        Returns
        -------
        CSIResult
            CSI value and status
        """
        # Convert symmetry to numeric
        Sy_num = self._symmetry_to_numeric(Sy)
        
        # Collect parameters
        params = {
            'K0': K0,
            'Vs': Vs,
            'Kprime': Kprime,
            'Sy': Sy_num,
            'alpha': alpha,
            'gamma': gamma
        }
        
        if U_lattice is not None:
            params['U_lattice'] = U_lattice
        else:
            # Default if not provided
            params['U_lattice'] = 15000
        
        # Normalize parameters
        normalized = {}
        for key, value in params.items():
            if key in self.weights:
                normalized[key] = self._normalize_parameter(key, value, mineral)
        
        # Calculate CSI
        csi = 0.0
        for key in normalized:
            csi += self.weights[key] * normalized[key]
        
        # Determine status
        if csi >= self.CSI_TRANSITION:
            status = "TRANSITION IMMINENT"
        elif csi >= self.CSI_STABLE:
            status = "METASTABLE"
        else:
            status = "STABLE"
        
        return CSIResult(
            csi=csi,
            status=status,
            normalized_params=normalized,
            weights=self.weights.copy()
        )
    
    def phase_boundary(
        self,
        mineral_a: str,
        mineral_b: str,
        P_range: Tuple[float, float] = (0, 150),
        T_range: Tuple[float, float] = (300, 3000),
        resolution: int = 50
    ) -> Dict:
        """
        Calculate phase boundary between two minerals
        
        Parameters
        ----------
        mineral_a, mineral_b : str
            Mineral names
        P_range : tuple
            Pressure range (GPa)
        T_range : tuple
            Temperature range (K)
        resolution : int
            Grid resolution
            
        Returns
        -------
        dict
            Phase boundary data
        """
        # This will be implemented when mineral database is ready
        # For now, return placeholder
        return {
            "mineral_a": mineral_a,
            "mineral_b": mineral_b,
            "status": "Not implemented - requires mineral database"
        }
    
    def plot_stability_map(
        self,
        mineral: str,
        P_range: Tuple[float, float] = (0, 150),
        T_range: Tuple[float, float] = (300, 3000),
        resolution: int = 100
    ):
        """
        Plot P-T stability map with CSI contours
        
        Parameters
        ----------
        mineral : str
            Mineral name
        P_range : tuple
            Pressure range (GPa)
        T_range : tuple
            Temperature range (K)
        resolution : int
            Grid resolution
        """
        # Placeholder - matplotlib would be needed for actual plotting
        print(f"📊 Stability map for {mineral} (plotting requires matplotlib)")
        print(f"   P range: {P_range[0]}-{P_range[1]} GPa")
        print(f"   T range: {T_range[0]}-{T_range[1]} K")
        print("   To generate actual plots, install matplotlib")
    
    def print_csi(self, result: CSIResult, mineral: str = ""):
        """Print formatted CSI result"""
        name = f" for {mineral}" if mineral else ""
        print("\n" + "="*50)
        print(f"🔮 Crystal Stability Index{name}")
        print("="*50)
        print(f"CSI = {result.csi:.3f}")
        print(f"Status: {result.status}")
        print("\nNormalized Parameters:")
        for param, value in sorted(result.normalized_params.items()):
            weight = result.weights.get(param, 0)
            print(f"  {param}: {value:.3f} (weight: {weight:.2f})")
        print("="*50)
