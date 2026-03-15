"""
Grüneisen parameter calculations and consistency checks
"""

import numpy as np
from typing import Optional, Tuple


def gruneisen_thermodynamic(
    alpha: float,
    K0: float,
    Vs: float,
    Cv: float
) -> float:
    """
    Thermodynamic Grüneisen parameter
    
    γ = α·K₀·V_s / C_v
    
    Parameters
    ----------
    alpha : float
        Thermal expansion coefficient (K⁻¹)
    K0 : float
        Isothermal bulk modulus (GPa)
    Vs : float
        Specific volume (cm³/mol)
    Cv : float
        Heat capacity at constant volume (J/mol·K)
    
    Returns
    -------
    float
        Grüneisen parameter γ
    """
    # Unit conversion: 1 GPa·cm³/mol = 0.1 J/mol
    return alpha * (K0 * Vs * 0.1) / Cv


def gruneisen_phonon(
    frequencies: np.ndarray,
    d_frequencies_dV: np.ndarray,
    weights: Optional[np.ndarray] = None
) -> float:
    """
    Phonon Grüneisen parameter from mode frequencies
    
    γ_i = -∂(ln ω_i)/∂(ln V)
    γ = Σ_i C_i·γ_i / Σ_i C_i
    
    Parameters
    ----------
    frequencies : array
        Phonon mode frequencies
    d_frequencies_dV : array
        Frequency derivatives with respect to volume
    weights : array, optional
        Mode heat capacities (if None, equal weights)
    
    Returns
    -------
    float
        Average phonon Grüneisen parameter
    """
    # Mode Grüneisen parameters
    gamma_i = -d_frequencies_dV * frequencies / frequencies  # ∂(ln ω)/∂(ln V)
    
    if weights is None:
        # Simple average
        return np.mean(gamma_i)
    else:
        # Weighted average by mode heat capacities
        return np.sum(weights * gamma_i) / np.sum(weights)


def gruneisen_volume_dependence(
    gamma0: float,
    V0: float,
    V: float,
    q: float = 1.5
) -> float:
    """
    Volume dependence of Grüneisen parameter
    
    γ(V) = γ₀ · (V/V₀)^q
    
    Parameters
    ----------
    gamma0 : float
        Grüneisen at reference volume
    V0 : float
        Reference volume
    V : float
        Current volume
    q : float
        Exponent (typically 1-2)
    
    Returns
    -------
    float
        Grüneisen at volume V
    """
    return gamma0 * (V0 / V) ** q


def consistency_check(
    gamma_thermo: float,
    gamma_phonon: float,
    tolerance: float = 0.15
) -> Tuple[bool, float]:
    """
    Check consistency between thermodynamic and phonon Grüneisen
    
    Parameters
    ----------
    gamma_thermo : float
        Grüneisen from thermodynamic definition
    gamma_phonon : float
        Grüneisen from phonon frequencies
    tolerance : float
        Maximum allowed discrepancy
    
    Returns
    -------
    Tuple[bool, float]
        (is_consistent, discrepancy)
    """
    discrepancy = abs(gamma_thermo - gamma_phonon)
    is_consistent = discrepancy <= tolerance
    
    return is_consistent, discrepancy


def acoustic_gruneisen(
    vp: float,
    vs: float,
    K0: float,
    rho: float
) -> float:
    """
    Acoustic Grüneisen parameter from seismic velocities
    
    γ_acoustic = (β_P + 2β_S)/3 where β are logarithmic derivatives
    
    Parameters
    ----------
    vp : float
        P-wave velocity (km/s)
    vs : float
        S-wave velocity (km/s)
    K0 : float
        Bulk modulus (GPa)
    rho : float
        Density (g/cm³)
    
    Returns
    -------
    float
        Acoustic Grüneisen approximation
    """
    # This is a simplified version
    # Full calculation requires pressure derivatives
    return (K0 / (rho * vp**2)) * 0.5  # Placeholder
