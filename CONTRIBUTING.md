
# Changelog

All notable changes to the MINERALCO project will be documented in this file.

**DOI:** 10.5281/zenodo.19009597  
**Repository:** github.com/gitedeeper9/mineralco  
**Web Dashboard:** mineralco.netlify.app

---

## [1.0.0] - 2026-03-14

### 🚀 Initial Release
- Publication of MINERALCO research paper
- Release of complete 7-parameter Crystal Intelligence Septuplet (CIS) framework
- 47 benchmark minerals validated against 3,200 experimental P-V-T data points
- CSI (Crystal Stability Index) formulation for phase transition prediction
- Open access data from synchrotron DAC and multi-anvil press experiments

### Added

#### Core Physics Engine
- **Bulk Modulus (K₀)** : Foundational measure of volumetric compressibility
  - Range: 108 GPa (enstatite) to 313 GPa (stishovite)
  - Bridgmanite: 261 ± 4 GPa
  - Validation against 3,200 experimental points

- **Lattice Parameters (a, b, c, α, β, γ)** : Crystallographic unit cell geometry
  - Full triclinic volume calculation: V = abc·√(1 - cos²α - cos²β - cos²γ + 2cosα·cosβ·cosγ)
  - Automated symmetry classification (230 space groups)
  - Anisotropic axial compression tracking

- **Pressure Derivative (K')** : Non-linear stiffening rate
  - K' = ∂K/∂P at P=0
  - Cubic minerals: 4.01 ± 0.24
  - Triclinic minerals: 4.91 ± 0.61
  - S_y-K' correlation (r = -0.88)

- **Crystal Symmetry (S_y)** : Space group classification
  - 7 crystal systems, 32 point groups, 230 space groups
  - Neumann's principle enforcement
  - Madelung constant determination for lattice energy

- **Thermal Expansion (α)** : Volumetric temperature response
  - α(T) = α₀ + α₁T + α₂T⁻² [Fei, 1995]
  - Range: 1.4×10⁻⁵ to 3.5×10⁻⁵ K⁻¹
  - Critical for mantle adiabat calculations

- **Grüneisen Parameter (γ)** : Thermodynamic coupling
  - γ = αK₀V/C_v = -∂(ln ω)/∂(ln V)
  - Thermodynamic vs. phonon consistency: r² = 0.971
  - Range: 1.0 - 2.0 (mantle minerals)

- **Specific Volume (V_s)** : Pressure-dependent molar volume
  - Primary observable in synchrotron experiments
  - From ambient to 363 GPa compression
  - Density calculation: ρ = M/V

#### Third-Order Birch-Murnaghan EOS (BM3-EOS)
- P(V) = (3K₀/2)·[(V₀/V)^(7/3) - (V₀/V)^(5/3)]·{1 + (3/4)(K'-4)·[(V₀/V)^(2/3) - 1]}
- Eulerian strain: f = [(V₀/V)^(2/3) - 1]/2
- Valid for compressions up to 50% (0-363 GPa)

#### Mie-Grüneisen Thermal Correction
- P_th(V,T) = γ(V)/V·[E_th(V,T) - E_th(V,T_ref)]
- E_th(V,T) = 9nRT·(T/θ_D)³·∫[θ_D/T to ∞] x³/(e^x - 1) dx [Debye model]
- θ_D(V) = θ_D0·(V₀/V)^γ

#### Born-Landé Lattice Energy
- U_L = -(N_A·M·Z⁺·Z⁻·e²)/(4πε₀·r₀)·(1 - 1/n)
- Madelung constant M determined by S_y
- Connects S_y, lattice parameters, and V_s

#### Crystal Stability Index (CSI)
- CSI = w₁·K₀* + w₂·V_s* + w₃·K'* + w₄·S_y* + w₅·α* + w₆·γ* + w₇·Φ_latt*
- Weights: w₁=0.28, w₂=0.19, w₃=0.17, w₄=0.13, w₅=0.10, w₆=0.09, w₇=0.04
- CSI ≥ 0.85: phase transition imminent (within ±2 GPa)
- CSI 0.65-0.85: metastable
- CSI < 0.65: stable

#### Processing Pipeline
- **EOSFitter**: BM3/BM4 EOS fitting engine
  - Non-linear least squares (Levenberg-Marquardt)
  - Covariance matrix analysis
  - 1σ uncertainty propagation

- **ThermalCorrector**: Mie-Grüneisen thermal EOS
  - Debye thermal energy model
  - γ(V) = γ₀·(V/V₀)^q volume dependence
  - Valid to 5,000 K

- **LatticeAnalyzer**: Unit cell geometry
  - Automated symmetry classification (tolerance: 0.5%)
  - Anisotropic axial compressibility ratios
  - Born-Landé lattice energy estimation

- **PhaseMapper**: Phase boundary and CSI module
  - Intersects EOS curves of competing phases
  - Clausius-Clapeyron slope: dP/dT = ΔS/ΔV
  - CSI colour-coded phase stability maps

#### Validation Dataset
- **Minerals**: 47 mantle and core phases
- **Data Points**: 3,200 P-V-T measurements
- **Pressure Range**: 0 - 363 GPa
- **Temperature Range**: 300 - 5,000 K
- **Sources**: MINERAL database + 3,200 published DAC/MAP experiments

#### Key Minerals Characterized

| Mineral | System | K₀ (GPa) | K' | Context |
|---------|--------|----------|-----|---------|
| Forsterite Mg₂SiO₄ | Orthorhombic | 128.4 | 4.31 | Upper mantle olivine |
| Wadsleyite β-Mg₂SiO₄ | Monoclinic | 172.3 | 4.26 | 410-520 km transition |
| Ringwoodite γ-Mg₂SiO₄ | Cubic | 185.1 | 4.14 | 520-660 km transition |
| Bridgmanite MgSiO₃ | Orthorhombic | 260.7 | 3.97 | Lower mantle (38% vol) |
| Post-perovskite MgSiO₃ | Orthorhombic | 229.8 | 4.02 | D" layer |
| Ferropericlase (Mg,Fe)O | Cubic | 162.3 | 3.84 | Lower mantle co-phase |
| ε-Iron hcp-Fe | Hexagonal | 163.4 | 5.38 | Inner core |

#### Phase Transition Predictions

| Transition | P_exp (GPa) | P_MINERALCO | CSI | Discontinuity |
|------------|-------------|-------------|-----|---------------|
| Olivine → Wadsleyite | 13.5 | 13.8 | 0.86 | 410 km |
| Wadsleyite → Ringwoodite | 18.0 | 18.3 | 0.88 | 520 km |
| Ringwoodite → Bridgmanite+FP | 23.5 | 23.2 | 0.91 | 660 km |
| Bridgmanite → Post-perovskite | 125 | 124 | 0.87 | D" layer |
| ε-Fe → Liquid Iron | 330 | 327 | 0.93 | Inner core boundary |

#### Performance Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| RMS Volumetric Error (all minerals) | 0.19% | ≤0.30% | ✅ |
| RMS Error (cubic minerals) | 0.09% | ≤0.20% | ✅ |
| RMS Error (orthorhombic) | 0.22% | ≤0.30% | ✅ |
| RMS Error (triclinic) | 0.29% | ≤0.35% | ✅ |
| Phase Transition Accuracy (43/47) | 91.5% | ≥90% | ✅ |
| CSI at Transition (mean) | 0.88 | ≥0.85 | ✅ |
| S_y-K' Correlation | r = -0.88 | p < 0.001 | ✅ |
| Grüneisen Consistency (r²) | 0.971 | ≥0.95 | ✅ |
| Bridgmanite V_P vs. PREM | 0.4% | ≤1.0% | ✅ |
| Bridgmanite V_S vs. PREM | <0.1% | ≤1.0% | ✅ |

#### Data Integration
- MINERAL Database (Stixrude & Lithgow-Bertelloni, 2011)
- NIST Crystal Data Database
- 3,200 published DAC/MAP experimental points (2000-2025)
- RRUFF Raman/IR spectral database

#### Deployment Options
- Single-mineral analysis
- Multi-mineral batch processing
- Real-time P-V-T calculation
- Docker containers
- Netlify web dashboard
- PyPI package: `pip install mineralco`

#### Documentation
- Complete API reference
- Installation guide (INSTALL.md)
- Deployment guide (DEPLOY.md)
- Contributing guidelines (CONTRIBUTING.md)
- Code of conduct (CODE_OF_CONDUCT.md)
- Jupyter notebooks for all case studies
- Parameter calibration protocols

---

## [0.9.0] - 2026-02-20

### ⚠️ Pre-release Candidate

### Added
- Beta version of all core modules
- Validation against 2,500 experimental points
- Preliminary CSI weight determination
- Basic data loaders
- Initial documentation

### Changed
- Refined BM3 fitting algorithms
- Updated Grüneisen parameter calculations
- Improved symmetry classification

### Fixed
- LatticeAnalyzer edge cases
- Thermal correction convergence
- Covariance matrix calculations

---

## [0.8.0] - 2026-01-25

### 🧪 Alpha Release

### Added
- Prototype physics modules
- Test deployments with MINERAL database
- Basic data collection pipeline
- Preliminary CSI formulation
- Initial mineral case studies

---

## [0.5.0] - 2025-10-10

### 🏗️ Development Milestone

### Added
- BM3 EOS implementation
- Basic lattice parameter handling
- Unit cell volume calculations
- Data ingestion from MINERAL database

---

## [0.1.0] - 2025-07-01

### 🎯 Project Initiation

### Added
- Project concept and framework design
- Initial 7-parameter selection
- Literature review compilation
- Research proposal development
- Data access agreements

---

## 🔮 Future Releases

### [1.1.0] - Planned Q4 2026
- Iron substitution effects module
- Spin-state crossover for Fe-bearing phases
- Additional validation (2026 data)
- Machine learning emulators for fast inversion
- Hydrous phase stability

### [1.2.0] - Planned Q2 2027
- Melt EOS module (partial melting)
- Grain-scale averaging (Voigt-Reuss-Hill)
- Elastic tensor visualization
- Enhanced anisotropy calculations

### [2.0.0] - Planned 2028
- Full thermodynamic database (500+ minerals)
- AI-powered phase transition prediction
- Real-time experimental data integration
- Planetary interior modelling (Mars, Venus, Exoplanets)
- 100+ mineral validation

---

## 📊 Version History

| Version | Date | Status | DOI |
|---------|------|--------|-----|
| 1.0.0 | 2026-03-14 | Stable Release | 10.5281/zenodo.19009597 |
| 0.9.0 | 2026-02-20 | Release Candidate | 10.5281/zenodo.18909597 |
| 0.8.0 | 2026-01-25 | Alpha | 10.5281/zenodo.18809597 |
| 0.5.0 | 2025-10-10 | Development | - |
| 0.1.0 | 2025-07-01 | Concept | - |

---

For questions or contributions: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0029
EOF

echo "✅ تم تعديل CHANGELOG.md"
```

---

الملف 11: CODE_OF_CONDUCT.md

```bash
cat > CODE_OF_CONDUCT.md << 'EOF'
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in the
MINERALCO project and our community a harassment-free experience for everyone,
regardless of age, body size, visible or invisible disability, ethnicity, sex
characteristics, gender identity and expression, level of experience,
education, socio-economic status, nationality, personal appearance, race,
religion, or sexual identity and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment for our
community include:

* Demonstrating empathy and kindness toward other people
* Being respectful of differing opinions, viewpoints, and experiences
* Giving and gracefully accepting constructive feedback
* Accepting responsibility and apologizing to those affected by our mistakes,
  and learning from the experience
* Focusing on what is best not just for us as individuals, but for the
  overall community
* Acknowledging the importance of mineral physics and Earth science research
* Promoting open science and reproducible research practices

Examples of unacceptable behavior include:

* The use of sexualized language or imagery, and sexual attention or
  advances of any kind
* Trolling, insulting or derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or email
  address, without their explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting
* Data manipulation or misrepresentation in scientific results

## Enforcement Responsibilities

Community leaders are responsible for clarifying and enforcing our standards of
acceptable behavior and will take appropriate and fair corrective action in
response to any behavior that they deem inappropriate, threatening, offensive,
or harmful.

Community leaders have the right and responsibility to remove, edit, or reject
comments, commits, code, wiki edits, issues, and other contributions that are
not aligned to this Code of Conduct, and will communicate reasons for moderation
decisions when appropriate.

## Scope

This Code of Conduct applies within all community spaces, and also applies when
an individual is officially representing the community in public spaces.
Examples of representing our community include using an official e-mail address,
posting via an official social media account, or acting as an appointed
representative at an online or offline event.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders responsible for enforcement at:
**gitdeeper@gmail.com**

All complaints will be reviewed and investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of the
reporter of any incident.

## Enforcement Guidelines

Community leaders will follow these Community Impact Guidelines in determining
the consequences for any action they deem in violation of this Code of Conduct:

### 1. Correction

**Community Impact**: Use of inappropriate language or other behavior deemed
unprofessional or unwelcome in the community.

**Consequence**: A private, written warning from community leaders, providing
clarity around the nature of the violation and an explanation of why the
behavior was inappropriate. A public apology may be requested.

### 2. Warning

**Community Impact**: A violation through a single incident or series of
actions.

**Consequence**: A warning with consequences for continued behavior. No
interaction with the people involved, including unsolicited interaction with
those enforcing the Code of Conduct, for a specified period of time. This
includes avoiding interactions in community spaces as well as external channels
like social media. Violating these terms may lead to a temporary or permanent
ban.

### 3. Temporary Ban

**Community Impact**: A serious violation of community standards, including
sustained inappropriate behavior.

**Consequence**: A temporary ban from any sort of interaction or public
communication with the community for a specified period of time. No public or
private interaction with the people involved, including unsolicited interaction
with those enforcing the Code of Conduct, is allowed during this period.
Violating these terms may lead to a permanent ban.

### 4. Permanent Ban

**Community Impact**: Demonstrating a pattern of violation of community
standards, including sustained inappropriate behavior, harassment of an
individual, or aggression toward or disparagement of classes of individuals.

**Consequence**: A permanent ban from any sort of public interaction within
the community.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.0, available at
https://www.contributor-covenant.org/version/2/0/code_of_conduct.html.

Community Impact Guidelines were inspired by [Mozilla's code of conduct
enforcement ladder](https://github.com/mozilla/diversity).

[homepage]: https://www.contributor-covenant.org

For answers to common questions about this code of conduct, see the FAQ at
https://www.contributor-covenant.org/faq. Translations are available at
https://www.contributor-covenant.org/translations.
EOF

echo "✅ تم تعديل CODE_OF_CONDUCT.md"
```

---

الملف 12: CONTRIBUTING.md

```bash
cat > CONTRIBUTING.md << 'EOF'
# 🤝 Contributing to MINERALCO

## Mineral Intelligence Network for Equation-of-state Research, Atomic Lattice COmputation

**DOI**: 10.5281/zenodo.19009597  
**Repository**: github.com/gitedeeper9/mineralco  
**Web**: mineralco.netlify.app

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Contributing to Physics Modules](#contributing-to-physics-modules)
- [Contributing to Data Processing](#contributing-to-data-processing)
- [Contributing to Documentation](#contributing-to-documentation)
- [Testing Guidelines](#testing-guidelines)
- [Data Contributions](#data-contributions)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

### Our Pledge
We as members, contributors, and leaders pledge to make participation in the MINERALCO community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members
- Acknowledging the importance of mineral physics and Earth science research
- Promoting open science and reproducible research

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at gitdeeper@gmail.com. All complaints will be reviewed and investigated promptly and fairly.

---

## 🚀 Getting Started

### Prerequisites
```bash
# Install development dependencies
python --version  # 3.9-3.11 required
git --version     # 2.30+ recommended
docker --version  # 20.10+ for containerized development
```

Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/mineralco.git
cd mineralco

# Add upstream remote
git remote add upstream https://github.com/gitedeeper9/mineralco.git
```

Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install --upgrade pip
pip install -e .[dev]
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial setup
python scripts/init_dev.py
```

Development Tools

```bash
# Code formatting
black mineralco/ tests/
isort mineralco/ tests/

# Linting
flake8 mineralco/ tests/ --max-line-length=100
pylint mineralco/ tests/

# Type checking
mypy mineralco/ --ignore-missing-imports

# Testing
pytest tests/ -v --cov=mineralco --numprocesses=auto
```

---

🔄 Development Workflow

Branch Naming Convention

```
feature/        # New features (e.g., feature/iron-substitution)
bugfix/         # Bug fixes (e.g., bugfix/bm3-convergence)
docs/           # Documentation (e.g., docs/api-refactor)
physics/        # Physics module updates (e.g., physics/gruneisen-q)
data/           # Data contributions (e.g., data/new-mineral-2026)
parameter/      # Parameter updates (e.g., parameter/csi-weights)
```

Development Process

```bash
# 1. Update your main branch
git checkout main
git pull upstream main

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes
# ... code changes ...

# 4. Run tests locally
pytest tests/ -v

# 5. Commit with conventional commit message
git add .
git commit -m "feat: add iron substitution module for bridgmanite"

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Create Pull Request on GitHub
```

Commit Message Convention

We follow Conventional Commits with scientific context:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:

· feat: New feature
· fix: Bug fix
· docs: Documentation only
· style: Code style (formatting)
· refactor: Code change that neither fixes bug nor adds feature
· perf: Performance improvement
· test: Adding missing tests
· physics: Changes to physics equations or parameters
· data: Data additions or updates
· parameter: Parameter or weight updates

Examples:

```
feat(bm3): add BM4 EOS with K'' free parameter
fix(lattice): correct triclinic volume calculation for angles > 90°
docs(csi): update threshold values based on 47-mineral validation
physics: refine Grüneisen parameter volume dependence γ(V) = γ₀·(V/V₀)^q
data: add 2026 synchrotron DAC data for bridgmanite at 130 GPa
parameter: update CSI weights based on PCA regression
```

---

🔬 Contributing to Physics Modules

Core Physics Equations

MINERALCO is built on seven governing equations from the research paper:

```python
# mineralco/physics/bm3.py
def birch_murnaghan_3rd_order(V0, K0, Kprime, V):
    """
    Third-Order Birch-Murnaghan Equation of State
    
    P(V) = (3K0/2)·[(V0/V)^(7/3) - (V0/V)^(5/3)]·
           {1 + (3/4)(K'-4)·[(V0/V)^(2/3) - 1]}
    
    Parameters
    ----------
    V0 : float
        Reference volume at zero pressure (cm³/mol)
    K0 : float
        Isothermal bulk modulus at zero pressure (GPa)
    Kprime : float
        Pressure derivative of bulk modulus at zero pressure
        K' = (∂K/∂P)_P=0
    V : float or array
        Volume at pressure P (cm³/mol)
    
    Returns
    -------
    float or array
        Pressure P (GPa)
    
    Notes
    -----
    - Valid for compressions up to 50% (f ≈ 0.35)
    - Reduces to Hooke's Law P = 3K0f at infinitesimal strain
    - For K' = 4 exactly, the equation simplifies to the original
      Birch-Murnaghan form without the correction term
    """
    f = ((V0 / V) ** (2/3) - 1) / 2  # Eulerian strain
    
    P = 3 * K0 * f * (1 + 2*f) ** (5/2) * (1 + 3/2 * (Kprime - 4) * f)
    
    return P
```

```python
# mineralco/physics/mie_gruneisen.py
def mie_gruneisen_thermal_pressure(V, T, T_ref, gamma0, q, theta_D0, n_atoms):
    """
    Mie-Grüneisen Thermal Pressure Correction
    
    P_th(V,T) = γ(V)/V · [E_th(V,T) - E_th(V,T_ref)]
    γ(V) = γ₀ · (V/V₀)^q
    E_th(V,T) = 9nRT · (T/θ_D)³ · ∫[θ_D/T to ∞] x³/(e^x - 1) dx
    
    Parameters
    ----------
    V : float
        Volume (cm³/mol)
    T : float
        Temperature (K)
    T_ref : float
        Reference temperature (usually 300 K)
    gamma0 : float
        Grüneisen parameter at reference volume
    q : float
        Volume dependence exponent (typically 1-2)
    theta_D0 : float
        Debye temperature at reference volume (K)
    n_atoms : int
        Number of atoms per formula unit
    
    Returns
    -------
    float
        Thermal pressure (GPa)
    
    Notes
    -----
    - Thermal pressure adds to isothermal BM3 pressure
    - Valid to approximately 5,000 K
    - Debye model accurate for most mantle minerals
    """
    # Volume-dependent Debye temperature
    theta_D = theta_D0 * (V / V0) ** (-gamma0)
    
    # Debye thermal energy (implementation simplified here)
    # Full implementation uses numerical integration of Debye function
    
    return P_th
```

```python
# mineralco/physics/symmetry.py
def classify_crystal_system(a, b, c, alpha, beta, gamma, tolerance=0.005):
    """
    Classify crystal system from lattice parameters
    
    Parameters
    ----------
    a, b, c : float
        Unit cell edge lengths (Å)
    alpha, beta, gamma : float
        Unit cell angles (degrees)
    tolerance : float
        Relative tolerance for equality comparisons (default: 0.5%)
    
    Returns
    -------
    str
        Crystal system: cubic, tetragonal, hexagonal, orthorhombic,
                       monoclinic, triclinic
    
    Notes
    -----
    Implements hierarchical classification:
    1. Check cubic (a=b=c, α=β=γ=90°)
    2. Check tetragonal (a=b≠c, α=β=γ=90°)
    3. Check hexagonal (a=b≠c, α=β=90°, γ=120°)
    4. Check orthorhombic (α=β=γ=90°, a≠b≠c)
    5. Check monoclinic (α=γ=90°, β≠90°)
    6. Default to triclinic
    """
    # Implementation follows hierarchical testing
    
    return crystal_system
```

```python
# mineralco/physics/gruneisen.py
def compute_gruneisen_parameter(alpha, K0, Vs, Cv):
    """
    Compute Grüneisen parameter from thermodynamic identity
    
    γ = α·K₀·V_s / C_v
    
    Parameters
    ----------
    alpha : float
        Volumetric thermal expansion coefficient (K⁻¹)
    K0 : float
        Isothermal bulk modulus (GPa)
    Vs : float
        Specific volume (cm³/mol)
    Cv : float
        Isochoric heat capacity (J/mol·K)
    
    Returns
    -------
    float
        Grüneisen parameter γ
    
    Notes
    -----
    - Typical range for mantle minerals: 1.0 - 2.0
    - Bridgmanite: γ = 1.57 ± 0.08
    - Periclase: γ = 1.524
    """
    gamma = alpha * K0 * Vs / Cv
    return gamma
```

```python
# mineralco/physics/csi.py
def compute_crystal_stability_index(params, weights=None):
    """
    Compute Crystal Stability Index (CSI)
    
    CSI = w₁·K₀* + w₂·V_s* + w₃·K'* + w₄·S_y* + w₅·α* + w₆·γ* + w₇·Φ_latt*
    
    Default weights (PCA-regularized regression):
    w₁=0.28, w₂=0.19, w₃=0.17, w₄=0.13, w₅=0.10, w₆=0.09, w₇=0.04
    
    Parameters
    ----------
    params : dict
        Dictionary with keys: 'K0', 'Vs', 'Kprime', 'Sy', 'alpha', 'gamma', 'U_lattice'
    weights : dict, optional
        Custom weights for each parameter
    
    Returns
    -------
    float
        CSI value (0-1)
    
    Thresholds:
    - CSI < 0.65: STABLE - no phase transition expected
    - CSI 0.65-0.85: METASTABLE - transition possible with overstepping
    - CSI ≥ 0.85: TRANSITION IMMINENT - within ±2 GPa
    
    Current benchmark: mean CSI at transition = 0.88 ± 0.03
    """
    # Normalize each parameter to [0,1] based on phase transition boundaries
    
    default_weights = {'K0': 0.28, 'Vs': 0.19, 'Kprime': 0.17,
                       'Sy': 0.13, 'alpha': 0.10, 'gamma': 0.09,
                       'U_lattice': 0.04}
    
    w = weights or default_weights
    
    csi = sum(w[key] * normalized[key] for key in params)
    
    return csi
```

Adding New Physics Models

```python
# mineralco/physics/new_model.py
"""
Template for contributing new physics models
"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class NewModelConfig:
    """Configuration for new physics model"""
    parameter1: float
    parameter2: float
    calibration_factor: Optional[float] = 1.0
    uncertainty_bounds: Tuple[float, float] = (0.0, 1.0)

class NewPhysicsModel:
    """
    New physics model implementation
    
    References
    ----------
    [1] Author et al. (2026) - DOI: 10.xxxx/xxxxx
    [2] MINERALCO Research Paper - DOI: 10.5281/zenodo.19009597
    """
    
    def __init__(self, config: Dict):
        self.config = NewModelConfig(**config)
        self.validate_against_experiments()
    
    def compute(self, input_data: np.ndarray) -> float:
        """
        Compute model output
        
        Parameters
        ----------
        input_data : np.ndarray
            Input data
        
        Returns
        -------
        float
            Model output
        """
        # Implement your model here
        result = self.config.parameter1 * np.mean(input_data)
        return result * self.config.calibration_factor
    
    def validate_against_experiments(self):
        """Validate model against experimental DAC data"""
        # Load validation data from MINERAL database
        # Compare predictions with synchrotron measurements
        # Report validation metrics
        # Ensure RMS error ≤ 0.3% for acceptance
        pass
```

---

📊 Contributing to Data Processing

Data Loaders

```python
# mineralco/data/loaders/mineral_db.py
"""
MINERAL Database loader (Stixrude & Lithgow-Bertelloni, 2011)
"""

import pandas as pd
from typing import Optional

class MineralDatabaseLoader:
    """
    Loader for MINERAL thermodynamic database
    
    Provides EOS parameters for 47 mantle and core minerals
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir or "data/raw"
    
    def load_mineral(self, mineral_name: str) -> dict:
        """
        Load CIS parameters for a specific mineral
        
        Parameters
        ----------
        mineral_name : str
            Name of mineral (e.g., 'bridgmanite', 'forsterite')
        
        Returns
        -------
        dict
            CIS parameters: K0, Kprime, V0, alpha, gamma, symmetry, lattice
        """
        # Load from JSON database
        pass
    
    def load_all_minerals(self) -> pd.DataFrame:
        """Load all 47 benchmark minerals"""
        pass
```

```python
# mineralco/data/loaders/synchrotron.py
"""
Synchrotron DAC experimental data loader
"""

class SynchrotronDataLoader:
    """
    Loader for high-pressure synchrotron XRD data
    
    Handles P-V-T data from diamond anvil cell experiments
    """
    
    def load_experimental_data(self, mineral: str, 
                               pressure_range: tuple = None) -> pd.DataFrame:
        """
        Load experimental P-V-T data points
        
        Returns
        -------
        pd.DataFrame with columns: P, V, T, source, year
        """
        pass
```

---

🧪 Testing Guidelines

Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── physics/
│   │   ├── test_bm3.py
│   │   ├── test_mie_gruneisen.py
│   │   ├── test_symmetry.py
│   │   ├── test_gruneisen.py
│   │   └── test_csi.py
│   ├── data/
│   │   └── test_mineral_db.py
│   └── processors/
│       └── test_eos_fitter.py
├── integration/            # Integration tests
│   ├── test_full_pipeline.py
│   ├── test_phase_prediction.py
│   └── test_47_minerals.py
├── validation/             # Validation against experiments
│   ├── test_bridgmanite.py
│   ├── test_660km_transition.py
│   └── test_prem_comparison.py
└── conftest.py             # Shared fixtures
```

Writing Tests

```python
# tests/unit/physics/test_bm3.py
import pytest
import numpy as np
from mineralco.physics.bm3 import birch_murnaghan_3rd_order

class TestBirchMurnaghanEOS:
    """Test suite for BM3-EOS calculations"""
    
    def test_periclase_validation(self):
        """Test against periclase (MgO) experimental data"""
        
        # Periclase parameters
        V0 = 11.249  # cm³/mol
        K0 = 160.3   # GPa
        Kprime = 3.99
        
        # Test at various pressures
        pressures = [0, 10, 25, 50, 100, 150]
        
        for P in pressures:
            # Compute volume from BM3
            # Compare with experimental data
            # Assert error < 0.3%
            pass
    
    def test_kprime_sensitivity(self):
        """Test sensitivity to K' parameter"""
        
        V0 = 24.45  # bridgmanite
        K0 = 260.7
        
        # Same P, different K'
        V_K4 = birch_murnaghan_3rd_order(V0, K0, 4.0, P=50)
        V_K5 = birch_murnaghan_3rd_order(V0, K0, 5.0, P=50)
        
        # K'=5 should give smaller volume (stiffer at high P)
        assert V_K5 < V_K4
```

---

🌍 Data Contributions

Contributing New Mineral Data

If you have high-pressure experimental data for minerals:

1. Prepare your data in the required format:

```csv
# Required format for CSV export
mineral, P(GPa), V(cm³/mol), T(K), K0(GPa), K', source, year, DOI
bridgmanite, 25.3, 23.12, 300, 261.2, 3.98, "Murakami et al.", 2012, 10.1038/nature11004
...
```

1. Include metadata:

```yaml
dataset:
  mineral: "bridgmanite"
  formula: "MgSiO3"
  system: "orthorhombic"
  space_group: "Pbnm"
  experiment_type: "synchrotron XRD"
  pressure_range: "25-130 GPa"
  temperature_range: "300-2500 K"
  data_points: 394
  reference: "Murakami et al. (2012) Nature"
  doi: "10.1038/nature11004"
```

---

🔀 Pull Request Process

PR Checklist

· Code follows project style guide
· Tests added/updated and passing
· Documentation updated
· CHANGELOG.md updated
· All CI checks passing
· Physics changes validated against experiments (if applicable)
· RMS error ≤ 0.3% for EOS changes
· Phase prediction accuracy ≥ 90% for CSI changes

---

📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to MINERALCO! 🪨

For questions: gitdeeper@gmail.com 
· ORCID: 0009-0003-8903-0029
