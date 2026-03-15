"""
ThermalCorrector - Mie-Grüneisen thermal pressure correction
Lightweight version - No NumPy
"""

import math
from typing import Optional
from dataclasses import dataclass


@dataclass
class ThermalResult:
    """Thermal correction results"""
    P_thermal: float           # Thermal pressure (GPa)
    P_total: float              # Total pressure (GPa)
    V: float                    # Volume (cm³/mol)
    T: float                    # Temperature (K)
    gamma: float                # Grüneisen parameter at this V,T
    E_th: float                 # Thermal energy (J/mol)


class ThermalCorrector:
    """
    Mie-Grüneisen thermal pressure correction - Lightweight version
    
    P_th(V,T) = γ(V)/V · [E_th(V,T) - E_th(V,T_ref)]
    γ(V) = γ₀ · (V/V₀)^q
    """
    
    # Physical constants
    R = 8.314  # Gas constant (J/mol·K)
    
    def __init__(
        self,
        K0: float,
        Kprime: float,
        V0: float,
        gamma0: float,
        alpha0: float,
        T_ref: float = 300.0,
        q: float = 1.5,
        n_atoms: int = 5,
        theta_D0: Optional[float] = None
    ):
        """
        Initialize thermal corrector
        
        Parameters
        ----------
        K0 : float
            Isothermal bulk modulus at reference (GPa)
        Kprime : float
            Pressure derivative
        V0 : float
            Reference volume (cm³/mol)
        gamma0 : float
            Grüneisen parameter at reference
        alpha0 : float
            Thermal expansion coefficient at reference (K⁻¹)
        T_ref : float
            Reference temperature (K)
        q : float
            Volume dependence exponent for γ
        n_atoms : int
            Number of atoms per formula unit
        theta_D0 : float, optional
            Debye temperature at reference (K)
        """
        self.K0 = K0
        self.Kprime = Kprime
        self.V0 = V0
        self.gamma0 = gamma0
        self.alpha0 = alpha0
        self.T_ref = T_ref
        self.q = q
        self.n_atoms = n_atoms
        
        # Estimate Debye temperature if not provided
        if theta_D0 is None:
            # Rough estimate based on bulk modulus
            # θ_D ≈ 251 * (K₀·V₀^(1/3)/M)^(1/2) where M is mean atomic mass
            M_mean = 20.0  # Approximate for silicates
            self.theta_D0 = 251 * math.sqrt((K0 * V0 ** (1/3)) / M_mean)
        else:
            self.theta_D0 = theta_D0
    
    def gamma(self, V: float) -> float:
        """Volume-dependent Grüneisen parameter"""
        return self.gamma0 * (self.V0 / V) ** self.q
    
    def debye_function_integral(self, x: float) -> float:
        """
        Approximation of ∫[x to ∞] t³/(e^t - 1) dt
        
        Uses polynomial approximation for different regimes
        """
        if x <= 0:
            return math.pi**4 / 15  # D(∞) = π⁴/15 ≈ 6.4939
        
        if x < 0.1:
            # Small x expansion (high T)
            return (math.pi**4/15) - x**3/3 + x**4/8 - x**5/20 + x**6/72
        elif x > 10:
            # Large x expansion (low T) - integral ≈ x³ e^{-x}
            return x**3 * math.exp(-x) * (1 + 4/x + 12/x**2 + 24/x**3)
        else:
            # Intermediate - simple rational approximation
            # Fitted to numerical values
            return (math.pi**4/15) / (1 + 0.3*x + 0.05*x**2 + 0.01*x**3)
    
    def thermal_energy(self, V: float, T: float) -> float:
        """
        Thermal energy from Debye model
        
        E_th(V,T) = 9nRT · (T/θ_D)³ · ∫[θ_D/T to ∞] x³/(e^x - 1) dx
        """
        # Volume-dependent Debye temperature
        theta_D = self.theta_D0 * (self.V0 / V) ** self.gamma(V)
        
        # Debye integral
        x = theta_D / T
        integral = self.debye_function_integral(x)
        
        # Thermal energy
        E_th = 9 * self.n_atoms * self.R * T * (T / theta_D) ** 3 * integral
        
        return E_th
    
    def thermal_pressure(self, V: float, T: float) -> float:
        """
        Calculate thermal pressure
        
        P_th(V,T) = γ(V)/V · [E_th(V,T) - E_th(V,T_ref)]
        """
        gamma_val = self.gamma(V)
        E_th_T = self.thermal_energy(V, T)
        E_th_ref = self.thermal_energy(V, self.T_ref)
        
        # Convert J/mol to GPa·cm³/mol (1 J = 10⁶ GPa·cm³)
        P_th = gamma_val / V * (E_th_T - E_th_ref) * 1e-6
        
        return P_th
    
    def pressure(self, V: float, T: float, P_iso: Optional[float] = None) -> ThermalResult:
        """
        Calculate total pressure at given V and T
        
        Parameters
        ----------
        V : float
            Volume (cm³/mol)
        T : float
            Temperature (K)
        P_iso : float, optional
            Isothermal pressure from BM3 at reference T
            If None, calculated using Murnaghan approximation
            
        Returns
        -------
        ThermalResult
            Thermal and total pressure
        """
        # Calculate thermal pressure
        P_th = self.thermal_pressure(V, T)
        
        # If isothermal pressure not provided, use Murnaghan approximation
        if P_iso is None:
            # P = (K0/K') * [(V0/V)^K' - 1]
            ratio = self.V0 / V
            P_iso = (self.K0 / self.Kprime) * (ratio ** self.Kprime - 1)
        
        P_total = P_iso + P_th
        
        return ThermalResult(
            P_thermal=P_th,
            P_total=P_total,
            V=V,
            T=T,
            gamma=self.gamma(V),
            E_th=self.thermal_energy(V, T)
        )
    
    def volume_at_PT(self, P_target: float, T: float, max_iter: int = 20, tol: float = 0.01) -> float:
        """
        Find volume at given pressure and temperature using Newton-Raphson
        
        Parameters
        ----------
        P_target : float
            Target pressure (GPa)
        T : float
            Temperature (K)
        max_iter : int
            Maximum iterations
        tol : float
            Tolerance (GPa)
            
        Returns
        -------
        float
            Volume at P,T (cm³/mol)
        """
        # Initial guess from Murnaghan
        V = self.V0 * (1 + self.Kprime * P_target / self.K0) ** (-1/self.Kprime)
        
        for i in range(max_iter):
            result = self.pressure(V, T)
            f = result.P_total - P_target
            
            if abs(f) < tol:
                return V
            
            # Numerical derivative
            h = V * 1e-4
            result_h = self.pressure(V + h, T)
            df = (result_h.P_total - result.P_total) / h
            
            if abs(df) < 1e-10:
                break
                
            V = V - f / df
            
            # Ensure volume stays positive
            if V <= 0:
                V = self.V0 * 0.5
            if V > self.V0 * 2:
                V = self.V0 * 2
        
        return V
    
    def print_summary(self):
        """Print thermal parameters summary"""
        print("\n" + "="*50)
        print("🔥 ThermalCorrector Parameters")
        print("="*50)
        print(f"K₀       = {self.K0:.1f} GPa")
        print(f"K'       = {self.Kprime:.2f}")
        print(f"V₀       = {self.V0:.2f} cm³/mol")
        print(f"γ₀       = {self.gamma0:.3f}")
        print(f"α₀       = {self.alpha0:.2e} K⁻¹")
        print(f"θ_D0     = {self.theta_D0:.0f} K")
        print(f"q        = {self.q:.1f}")
        print(f"n_atoms  = {self.n_atoms}")
        print("="*50)
