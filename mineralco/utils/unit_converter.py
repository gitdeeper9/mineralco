"""
Unit conversion utilities for mineral physics
"""

import numpy as np


def GPa_to_bar(P: float) -> float:
    """Convert GPa to bar (1 GPa = 10,000 bar)"""
    return P * 10000


def bar_to_GPa(P: float) -> float:
    """Convert bar to GPa"""
    return P / 10000


def cm3_per_mol_to_Ang3_per_cell(V: float, z: int = 1) -> float:
    """
    Convert cm³/mol to Å³ per unit cell
    
    Parameters
    ----------
    V : float
        Molar volume (cm³/mol)
    z : int
        Formula units per cell
    
    Returns
    -------
    float
        Unit cell volume (Å³)
    """
    # 1 cm³/mol = 10²⁴ / N_A Å³ per formula unit
    # N_A = 6.02214076e23
    return V * 1.66053906660 * z


def Ang3_per_cell_to_cm3_per_mol(V_cell: float, z: int = 1) -> float:
    """
    Convert Å³ per unit cell to cm³/mol
    
    Parameters
    ----------
    V_cell : float
        Unit cell volume (Å³)
    z : int
        Formula units per cell
    
    Returns
    -------
    float
        Molar volume (cm³/mol)
    """
    return V_cell / (1.66053906660 * z)


def kg_per_m3_to_g_per_cm3(density: float) -> float:
    """Convert kg/m³ to g/cm³"""
    return density / 1000


def g_per_cm3_to_kg_per_m3(density: float) -> float:
    """Convert g/cm³ to kg/m³"""
    return density * 1000


def km_per_s_to_m_per_s(v: float) -> float:
    """Convert km/s to m/s"""
    return v * 1000


def m_per_s_to_km_per_s(v: float) -> float:
    """Convert m/s to km/s"""
    return v / 1000


def J_to_eV(E: float) -> float:
    """Convert Joules to electronvolts"""
    return E / 1.60217662e-19


def eV_to_J(E: float) -> float:
    """Convert electronvolts to Joules"""
    return E * 1.60217662e-19


def kJ_per_mol_to_eV_per_atom(E: float, n_atoms: int = 1) -> float:
    """
    Convert kJ/mol to eV/atom
    
    Parameters
    ----------
    E : float
        Energy in kJ/mol
    n_atoms : int
        Number of atoms per formula unit
    
    Returns
    -------
    float
        Energy in eV/atom
    """
    # 1 kJ/mol = 0.010364 eV/atom
    return E * 0.010364 / n_atoms


def eV_per_atom_to_kJ_per_mol(E: float, n_atoms: int = 1) -> float:
    """
    Convert eV/atom to kJ/mol
    
    Parameters
    ----------
    E : float
        Energy in eV/atom
    n_atoms : int
        Number of atoms per formula unit
    
    Returns
    -------
    float
        Energy in kJ/mol
    """
    return E * 96.485 * n_atoms
