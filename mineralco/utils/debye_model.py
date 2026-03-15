"""
Debye model for thermal energy and heat capacity
"""

import numpy as np
from scipy.integrate import quad
from typing import Optional


def debye_function_3(x: float) -> float:
    """
    Debye function integrand D(x) = x³/(e^x - 1)
    """
    if x < 1e-6:
        return 0.0
    return x**3 / (np.exp(x) - 1)


def debye_integral(x_min: float) -> float:
    """
    ∫[x_min to ∞] x³/(e^x - 1) dx
    """
    if x_min < 1e-6:
        # Small x_min approximation: integral ≈ 6.49394
        return 6.49394
    
    integral, _ = quad(debye_function_3, x_min, np.inf, limit=100)
    return integral


def thermal_energy_debye(
    T: float,
    theta_D: float,
    n_atoms: int,
    R: float = 8.314
) -> float:
    """
    Thermal energy from Debye model
    
    E_th = 9nRT · (T/θ_D)³ · ∫[θ_D/T to ∞] x³/(e^x - 1) dx
    
    Parameters
    ----------
    T : float
        Temperature (K)
    theta_D : float
        Debye temperature (K)
    n_atoms : int
        Number of atoms per formula unit
    R : float
        Gas constant (J/mol·K)
    
    Returns
    -------
    float
        Thermal energy (J/mol)
    """
    x_min = theta_D / T
    integral = debye_integral(x_min)
    
    E_th = 9 * n_atoms * R * T * (T / theta_D) ** 3 * integral
    return E_th


def heat_capacity_debye(
    T: float,
    theta_D: float,
    n_atoms: int,
    R: float = 8.314
) -> float:
    """
    Heat capacity from Debye model
    
    C_v = 9nR · (T/θ_D)³ · ∫[θ_D/T to ∞] x⁴ e^x / (e^x - 1)² dx
    
    Parameters
    ----------
    T : float
        Temperature (K)
    theta_D : float
        Debye temperature (K)
    n_atoms : int
        Number of atoms per formula unit
    R : float
        Gas constant (J/mol·K)
    
    Returns
    -------
    float
        Heat capacity at constant volume (J/mol·K)
    """
    if T < 1e-6:
        return 0.0
    
    # Low temperature limit: C_v ∝ T³
    if T < theta_D / 100:
        return 9 * n_atoms * R * (T / theta_D) ** 3 * 4 * np.pi**4 / 5
    
    # High temperature limit: C_v → 3nR
    if T > 10 * theta_D:
        return 3 * n_atoms * R
    
    # General case - numerical integration
    x_min = theta_D / T
    
    def integrand(x):
        if x < 1e-6:
            return 0.0
        return x**4 * np.exp(x) / (np.exp(x) - 1) ** 2
    
    integral, _ = quad(integrand, x_min, np.inf, limit=100)
    
    C_v = 9 * n_atoms * R * (T / theta_D) ** 3 * integral
    return C_v


def debye_temperature_from_bulk_modulus(
    K0: float,
    V0: float,
    M_mean: float,
    n_atoms: int
) -> float:
    """
    Estimate Debye temperature from bulk modulus
    
    θ_D ≈ 251 · (K₀·V₀^(1/3)/M_mean)^(1/2)
    
    Parameters
    ----------
    K0 : float
        Bulk modulus (GPa)
    V0 : float
        Molar volume (cm³/mol)
    M_mean : float
        Mean atomic mass (g/mol)
    n_atoms : int
        Number of atoms per formula unit
    
    Returns
    -------
    float
        Estimated Debye temperature (K)
    """
    # Convert V0 from cm³/mol to Å³ per atom
    V_atom = V0 * 1.66054 / n_atoms  # Å³ per atom
    
    return 251 * np.sqrt((K0 * V_atom ** (1/3)) / M_mean)
