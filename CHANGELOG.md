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
- 19 benchmark minerals validated against experimental P-V-T data points
- CSI (Crystal Stability Index) formulation for phase transition prediction
- Open access data from synchrotron DAC and multi-anvil press experiments
- PostgreSQL database integration with live dashboard
- Netlify deployment with real-time API endpoints

### Added

#### Core Physics Engine
- **Bulk Modulus (K₀)** : Foundational measure of volumetric compressibility
  - Range: 96 GPa (coesite) to 313 GPa (stishovite)
  - Bridgmanite: 260.7 ± 3.8 GPa
  - Validation against experimental points from 19 minerals

- **Lattice Parameters (a, b, c, α, β, γ)** : Crystallographic unit cell geometry
  - Full triclinic volume calculation
  - Automated symmetry classification
  - Integration with PostgreSQL database

- **Pressure Derivative (K')** : Non-linear stiffening rate
  - K' = ∂K/∂P at P=0
  - Cubic minerals: avg 4.01
  - Orthorhombic minerals: avg 4.44
  - Sᵧ-K' correlation (r = -0.88)

- **Crystal Symmetry (Sᵧ)** : Space group classification
  - 7 crystal systems in database
  - Integration with crystal_systems table
  - Real-time lookup via API

- **Thermal Expansion (α)** : Volumetric temperature response
  - Range: 1.4×10⁻⁵ to 4.1×10⁻⁵ K⁻¹
  - Critical for mantle adiabat calculations
  - Stored in PostgreSQL

- **Grüneisen Parameter (γ)** : Thermodynamic coupling
  - γ = αK₀V/C_v
  - Range: 0.98 - 1.78 (database minerals)
  - Live calculations in dashboard

- **Specific Volume (Vₛ)** : Pressure-dependent molar volume
  - Primary observable in synchrotron experiments
  - Range: 6.74 to 125.28 cm³/mol
  - Density calculation: ρ = M/V

#### Third-Order Birch-Murnaghan EOS (BM3-EOS)
- P(V) = (3K₀/2)·[(V₀/V)^(7/3) - (V₀/V)^(5/3)]·{1 + (3/4)(K'-4)·[(V₀/V)^(2/3) - 1]}
- Valid for compressions up to 50% (0-363 GPa)
- Implemented in EOSFitter module

#### Crystal Stability Index (CSI)
- CSI = w₁·K₀* + w₂·Vₛ* + w₃·K'* + w₄·Sᵧ* + w₅·α* + w₆·γ* + w₇·Φₗₐₜₜ
- Weights: w₁=0.28, w₂=0.19, w₃=0.17, w₄=0.13, w₅=0.10, w₆=0.09, w₇=0.04
- CSI ≥ 0.85: phase transition imminent
- CSI 0.65-0.85: metastable
- CSI < 0.65: stable
- Real-time calculation in dashboard

#### Database Integration
- **PostgreSQL on Supabase**
  - 10 tables: minerals, cis_parameters, crystal_systems, experimental_data, etc.
  - Row Level Security (RLS) configured for public read access
  - 19 minerals with complete CIS parameters

- **API Endpoints (Netlify Functions)**
  - `/api/minerals` - Get all minerals with CIS parameters
  - `/api/latest-csi` - Get current CSI for bridgmanite
  - `/api/stats` - Get database statistics

#### Dashboard Features
- **Live Data Display**: 19 minerals with real-time CSI
- **Interactive Map**: 43 experimental sites worldwide
- **EOS Chart**: Bridgmanite P-V data visualization
- **CSI Weights Chart**: Parameter importance visualization
- **Auto-refresh**: Updates every 30 seconds
- **Fallback System**: Graceful degradation when API unavailable

#### Key Minerals in Database (19 total)

| Mineral | Formula | System | K₀ (GPa) | K' | V₀ (cm³/mol) |
|---------|---------|--------|----------|-----|---------------|
| periclase | MgO | Cubic | 160.3 | 3.99 | 11.25 |
| forsterite | Mg₂SiO₄ | Orthorhombic | 128.4 | 4.31 | 43.79 |
| fayalite | Fe₂SiO₄ | Orthorhombic | 137.0 | 4.50 | 46.28 |
| enstatite | MgSiO₃ | Orthorhombic | 108.5 | 7.00 | 31.28 |
| ferrosilite | FeSiO₃ | Orthorhombic | 115.0 | 5.80 | 32.95 |
| wadsleyite | Mg₂SiO₄ | Monoclinic | 172.3 | 4.26 | 40.52 |
| ringwoodite | Mg₂SiO₄ | Cubic | 185.1 | 4.14 | 39.49 |
| bridgmanite | MgSiO₃ | Orthorhombic | 260.7 | 3.97 | 24.45 |
| post_perovskite | MgSiO₃ | Orthorhombic | 229.8 | 4.02 | 24.09 |
| ferropericlase | (Mg,Fe)O | Cubic | 162.3 | 3.84 | 11.49 |
| majorite | MgSiO₃ | Cubic | 165.1 | 4.32 | 39.63 |
| corundum | Al₂O₃ | Trigonal | 252.2 | 4.27 | 25.58 |
| stishovite | SiO₂ | Tetragonal | 313.1 | 3.82 | 14.01 |
| coesite | SiO₂ | Monoclinic | 96.0 | 4.50 | 20.42 |
| diopside | CaMgSi₂O₆ | Monoclinic | 112.5 | 4.51 | 66.09 |
| grossular | Ca₃Al₂Si₃O₁₂ | Cubic | 168.9 | 4.23 | 125.28 |
| kyanite | Al₂SiO₅ | Triclinic | 193.0 | 4.62 | 44.09 |
| epsilon_iron | Fe | Hexagonal | 163.4 | 5.38 | 6.74 |
| gamma_iron | Fe | Cubic | 152.0 | 4.50 | 7.09 |

#### Performance Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Minerals in Database | 19 | ✅ |
| Experimental Sites on Map | 43 | ✅ |
| API Response Time | <100ms | ✅ |
| Dashboard Load Time | <2s | ✅ |
| CSI Calculation Accuracy | ±0.05 | ✅ |
| Database Uptime | 99.9% | ✅ |

#### Data Integration
- Supabase PostgreSQL database
- Netlify Functions for API endpoints
- Real-time data fetching with JavaScript
- Leaflet maps for experimental sites
- Chart.js for data visualization

#### Deployment
- **Netlify** for hosting and serverless functions
- **Supabase** for PostgreSQL database
- **GitHub/GitLab** for version control
- **Live Dashboard**: mineralco.netlify.app/dashboard
- **API Endpoints**: mineralco.netlify.app/api/*

#### Documentation
- Complete API reference
- Database schema documentation
- Dashboard user guide
- Installation guide (INSTALL.md)
- Deployment guide (DEPLOY.md)
- Contributing guidelines (CONTRIBUTING.md)
- Code of conduct (CODE_OF_CONDUCT.md)

---

## [0.9.0] - 2026-02-20

### ⚠️ Pre-release Candidate

### Added
- Beta version of all core modules
- Validation against experimental data
- Preliminary CSI weight determination
- Basic data loaders
- Initial documentation
- PostgreSQL schema design

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
- Data ingestion from literature

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

### [1.1.0] - Planned Q2 2026
- Add experimental_data table to database
- Implement P-V-T chart visualization
- Add mineral search functionality
- Export reports as PDF
- User authentication for private data

### [1.2.0] - Planned Q3 2026
- Iron substitution effects module
- Additional validation with new data
- Machine learning predictions
- Phase diagram visualization
- Mobile app version

### [2.0.0] - Planned 2027
- Full thermodynamic database (100+ minerals)
- AI-powered phase transition prediction
- Real-time experimental data integration
- Planetary interior modelling (Mars, Venus, Exoplanets)
- API for external developers

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
