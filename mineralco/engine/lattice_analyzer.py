"""
LatticeAnalyzer - Unit cell geometry and symmetry classification
Lightweight version - No NumPy
"""

import math
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass


@dataclass
class LatticeResult:
    """Lattice analysis results"""
    crystal_system: str
    space_group: Optional[str]
    V0: float                    # Unit cell volume (Å³)
    V0_molar: float               # Molar volume (cm³/mol)
    density: float                # Density (g/cm³)
    madelung_constant: float      # Madelung constant
    K_prime_prior: Tuple[float, float]  # K' prior (mean, std)


class LatticeAnalyzer:
    """
    Unit cell geometry and crystal symmetry analysis
    
    - Classifies crystal system from lattice parameters
    - Calculates unit cell volume
    - Provides Madelung constants by symmetry
    - Estimates K' from symmetry (S_y-K' correlation)
    """
    
    # Crystal system classification thresholds
    TOLERANCE = 0.005  # 0.5% relative tolerance
    
    # Madelung constants by crystal system (approximate)
    MADELUNG_CONSTANTS = {
        "cubic_NaCl": 1.7476,
        "cubic_CsCl": 2.4078,
        "cubic_zincblende": 1.6381,
        "cubic_general": 1.75,
        "tetragonal": 1.60,
        "hexagonal": 1.64,
        "orthorhombic": 1.62,
        "monoclinic": 1.60,
        "triclinic": 1.58
    }
    
    # K' priors from S_y-K' correlation (H4 hypothesis)
    KPRIME_PRIORS = {
        "cubic": (4.01, 0.24),
        "tetragonal": (4.18, 0.31),
        "hexagonal": (4.29, 0.38),
        "trigonal": (4.29, 0.38),
        "orthorhombic": (4.44, 0.41),
        "monoclinic": (4.67, 0.52),
        "triclinic": (4.91, 0.61)
    }
    
    def __init__(
        self,
        a: float,
        b: Optional[float] = None,
        c: Optional[float] = None,
        alpha: float = 90.0,
        beta: float = 90.0,
        gamma: float = 90.0,
        tolerance: float = 0.005,
        formula_weight: Optional[float] = None,
        z: int = 1  # Formula units per cell
    ):
        """
        Initialize lattice analyzer
        
        Parameters
        ----------
        a, b, c : float
            Unit cell edge lengths (Å)
        alpha, beta, gamma : float
            Unit cell angles (degrees)
        tolerance : float
            Relative tolerance for equality comparisons
        formula_weight : float, optional
            Formula weight (g/mol) for density calculation
        z : int
            Number of formula units per cell
        """
        self.a = a
        self.b = b if b is not None else a
        self.c = c if c is not None else a
        self.alpha = math.radians(alpha)
        self.beta = math.radians(beta)
        self.gamma = math.radians(gamma)
        self.tolerance = tolerance
        self.formula_weight = formula_weight
        self.z = z
        
        # Classify crystal system
        self.crystal_system = self._classify_system()
        self.V0 = self._calculate_volume()
        
        # Convert Å³ to cm³/mol (1 Å³ = 10⁻²⁴ cm³, 1 mol = 6.022×10²³)
        # V0_molar = V0 (Å³/cell) * (10⁻²⁴ cm³/Å³) * (6.022×10²³ /mol) / (z formula units/cell)
        # Simplified: V0_molar = V0 * 0.602214076 / z
        self.V0_molar = self.V0 * 0.602214076 / self.z
        
        if formula_weight:
            # Density = (formula_weight * z) / (V0_molar)
            # V0_molar already accounts for z, so density = formula_weight / V0_molar
            self.density = formula_weight / self.V0_molar
        else:
            self.density = None
    
    def _almost_equal(self, x: float, y: float) -> bool:
        """Check if two values are equal within tolerance"""
        if abs(x) < 1e-6 and abs(y) < 1e-6:
            return True
        if max(abs(x), abs(y)) < 1e-6:
            return True
        return abs(x - y) / max(abs(x), abs(y), 1e-6) < self.tolerance
    
    def _classify_system(self) -> str:
        """
        Classify crystal system from lattice parameters
        
        Hierarchy:
        1. Cubic: a=b=c, α=β=γ=90°
        2. Tetragonal: a=b≠c, α=β=γ=90°
        3. Hexagonal: a=b≠c, α=β=90°, γ=120°
        4. Trigonal: a=b=c, α=β=γ≠90° (rhombohedral)
        5. Orthorhombic: α=β=γ=90°, a≠b≠c
        6. Monoclinic: α=γ=90°, β≠90°
        7. Triclinic: all others
        """
        a, b, c = self.a, self.b, self.c
        alpha, beta, gamma = self.alpha, self.beta, self.gamma
        
        # Convert to degrees for comparison
        alpha_deg = math.degrees(alpha)
        beta_deg = math.degrees(beta)
        gamma_deg = math.degrees(gamma)
        
        # Check cubic
        if (self._almost_equal(a, b) and self._almost_equal(a, c) and
            self._almost_equal(alpha_deg, 90) and
            self._almost_equal(beta_deg, 90) and
            self._almost_equal(gamma_deg, 90)):
            return "cubic"
        
        # Check tetragonal
        if (self._almost_equal(a, b) and not self._almost_equal(a, c) and
            self._almost_equal(alpha_deg, 90) and
            self._almost_equal(beta_deg, 90) and
            self._almost_equal(gamma_deg, 90)):
            return "tetragonal"
        
        # Check hexagonal
        if (self._almost_equal(a, b) and not self._almost_equal(a, c) and
            self._almost_equal(alpha_deg, 90) and
            self._almost_equal(beta_deg, 90) and
            self._almost_equal(gamma_deg, 120)):
            return "hexagonal"
        
        # Check trigonal (rhombohedral)
        if (self._almost_equal(a, b) and self._almost_equal(a, c) and
            self._almost_equal(alpha_deg, beta_deg) and
            self._almost_equal(alpha_deg, gamma_deg) and
            not self._almost_equal(alpha_deg, 90)):
            return "trigonal"
        
        # Check orthorhombic
        if (not self._almost_equal(a, b) and
            not self._almost_equal(a, c) and
            not self._almost_equal(b, c) and
            self._almost_equal(alpha_deg, 90) and
            self._almost_equal(beta_deg, 90) and
            self._almost_equal(gamma_deg, 90)):
            return "orthorhombic"
        
        # Check monoclinic
        if (self._almost_equal(alpha_deg, 90) and
            self._almost_equal(gamma_deg, 90) and
            not self._almost_equal(beta_deg, 90)):
            return "monoclinic"
        
        # Default to triclinic
        return "triclinic"
    
    def _calculate_volume(self) -> float:
        """
        Calculate unit cell volume for any crystal system
        
        V = a·b·c·√(1 - cos²α - cos²β - cos²γ + 2cosα·cosβ·cosγ)
        """
        cos_alpha = math.cos(self.alpha)
        cos_beta = math.cos(self.beta)
        cos_gamma = math.cos(self.gamma)
        
        # Calculate volume factor
        term = (1 - cos_alpha**2 - cos_beta**2 - cos_gamma**2 +
                2 * cos_alpha * cos_beta * cos_gamma)
        
        if term < 0:
            # Numerical error, take absolute value
            term = abs(term)
        
        volume_factor = math.sqrt(term)
        
        return self.a * self.b * self.c * volume_factor
    
    def get_madelung_constant(self, structure_type: str = "general") -> float:
        """
        Get Madelung constant based on crystal system
        
        Parameters
        ----------
        structure_type : str
            Specific structure type (e.g., "NaCl", "CsCl", "general")
        
        Returns
        -------
        float
            Madelung constant
        """
        key = f"{self.crystal_system}_{structure_type}"
        if key in self.MADELUNG_CONSTANTS:
            return self.MADELUNG_CONSTANTS[key]
        
        # Fallback to general value
        general_key = f"{self.crystal_system}_general"
        if general_key in self.MADELUNG_CONSTANTS:
            return self.MADELUNG_CONSTANTS[general_key]
        
        # Ultimate fallback
        return 1.6
    
    def get_kprime_prior(self) -> Tuple[float, float]:
        """
        Get K' prior from crystal symmetry (H4 hypothesis)
        
        Returns
        -------
        Tuple[float, float]
            (mean, standard deviation) for K'
        """
        return self.KPRIME_PRIORS.get(self.crystal_system, (4.5, 0.5))
    
    def born_lande_energy(
        self,
        Z_plus: int,
        Z_minus: int,
        r0: Optional[float] = None,
        n: float = 9.0,
        structure_type: str = "general"
    ) -> float:
        """
        Calculate Born-Landé lattice energy
        
        U_L = -(N_A·M·Z⁺·Z⁻·e²)/(4πε₀·r₀)·(1 - 1/n)
        
        Parameters
        ----------
        Z_plus, Z_minus : int
            Ionic charges
        r0 : float, optional
            Equilibrium interionic distance (Å)
            If None, estimated from cell volume
        n : float
            Born exponent (5-12, typical 9)
        structure_type : str
            Structure type for Madelung constant
        
        Returns
        -------
        float
            Lattice energy (kJ/mol)
        """
        # Constants
        N_A = 6.02214076e23  # Avogadro's number
        e = 1.60217662e-19  # Elementary charge (C)
        epsilon_0 = 8.8541878128e-12  # Vacuum permittivity (F/m)
        
        # Get Madelung constant
        M = self.get_madelung_constant(structure_type)
        
        # Estimate r0 if not provided
        if r0 is None:
            # Rough estimate: r0 ≈ (V0 / (number of ions))^(1/3)
            # For binary compound AB, ions per cell = 2*z
            ions_per_cell = 2 * self.z
            r0 = (self.V0 / ions_per_cell) ** (1/3)
        
        # Convert r0 from Å to m
        r0_m = r0 * 1e-10
        
        # Calculate lattice energy (J/mol)
        U_J = -(N_A * M * Z_plus * Z_minus * e**2) / (4 * math.pi * epsilon_0 * r0_m) * (1 - 1/n)
        
        # Convert to kJ/mol
        U_kJ = U_J / 1000
        
        return U_kJ
    
    def summary(self) -> Dict:
        """Return summary of lattice analysis"""
        result = {
            "crystal_system": self.crystal_system,
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "alpha_deg": math.degrees(self.alpha),
            "beta_deg": math.degrees(self.beta),
            "gamma_deg": math.degrees(self.gamma),
            "V0_Ang3": self.V0,
            "V0_cm3_per_mol": self.V0_molar,
            "kprime_prior_mean": self.get_kprime_prior()[0],
            "kprime_prior_std": self.get_kprime_prior()[1]
        }
        
        if self.density:
            result["density_g_per_cm3"] = self.density
        
        return result
