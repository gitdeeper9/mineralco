# 🪨 MINERALCO Installation Guide v1.0.0
## Mineral Intelligence Network for Equation-of-state Research, Atomic Lattice COmputation

**DOI**: 10.5281/zenodo.19009597  
**Repository**: github.com/gitedeeper9/mineralco  
**Web**: mineralco.netlify.app

---

## 📋 System Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04+, Debian 11+, macOS 12+, Windows 10/11 (WSL2)
- **RAM**: 8 GB
- **Storage**: 50 GB free space (for data)
- **Python**: 3.9 - 3.11
- **CPU**: 4+ cores

### Recommended Requirements
- **RAM**: 16+ GB
- **Storage**: 200+ GB SSD
- **CPU**: 8+ cores
- **Python**: 3.10

### Data Requirements
- **Internet connection** for downloading datasets
- **Total data size**: ~30-50 GB
- **Datasets**:
  - MINERAL Database: ~10 MB
  - Synchrotron DAC Data: ~5 GB
  - RRUFF Database: ~2 GB
  - NIST Crystal Data: ~500 MB

---

## 🚀 Quick Installation (5 minutes)

### 1. Install via pip (Recommended)

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install MINERALCO
pip install --upgrade pip
pip install mineralco

# Verify installation
python -c "import mineralco; print(mineralco.__version__)"
# Should output: 1.0.0
```

2. Quick Test

```bash
# Download sample data
mineralco-download-sample --output ./sample_data

# Process a mineral (e.g., bridgmanite)
mineralco-process --mineral bridgmanite --input ./sample_data --output ./results

# View CSI results
mineralco-csi --mineral bridgmanite --pressure 25 --temperature 2000
```

3. Start Web Dashboard

```bash
# Start local server
mineralco-serve --host 127.0.0.1 --port 5000

# Open browser: http://127.0.0.1:5000
```

---

📦 Installation Methods

Method A: pip Install (Production)

```bash
# Basic installation
pip install mineralco

# With all optional dependencies
pip install mineralco[all]

# With specific extras
pip install mineralco[docs]     # Documentation tools
pip install mineralco[dev]      # Development tools
pip install mineralco[web]      # Web dashboard
```

Method B: From Source (Development)

```bash
# Clone repository
git clone https://github.com/gitedeeper9/mineralco.git
cd mineralco

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v
```

Method C: Docker (Containerized)

```bash
# Pull from Docker Hub
docker pull gitedeeper9/mineralco:latest

# Run container
docker run -d \
  --name mineralco \
  -p 5000:5000 \
  -p 8000:8000 \
  -v $(pwd)/data:/data \
  -v $(pwd)/config:/app/config \
  gitedeeper9/mineralco:latest

# Or build locally
docker build -t mineralco:latest .
docker-compose up -d
```

---

🔧 Detailed Installation Steps

Step 1: System Dependencies

Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y \
  python3-pip \
  python3-dev \
  python3-venv \
  git \
  build-essential \
  libhdf5-dev \
  libnetcdf-dev \
  libopenblas-dev \
  libfftw3-dev
```

macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install \
  python@3.10 \
  git \
  hdf5 \
  netcdf \
  openblas \
  fftw
```

Step 2: Python Environment

```bash
# Create virtual environment
python3 -m venv ~/venv/mineralco
source ~/venv/mineralco/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

Step 3: Install MINERALCO

```bash
# Core installation
pip install mineralco

# Verify installation
python -c "
import mineralco
print(f'MINERALCO version: {mineralco.__version__}')
print(f'Core modules: {mineralco.__all__}')
"
```

Step 4: Configure Environment

```bash
# Create configuration directory
mkdir -p ~/.mineralco

# Download example configuration
curl -o ~/.mineralco/config.yaml \
  https://raw.githubusercontent.com/gitedeeper9/mineralco/main/config/config.yaml

# Edit configuration
nano ~/.mineralco/config.yaml
```

Step 5: Download Data

```bash
# Create data directory
mkdir -p ~/mineralco_data

# Download MINERAL database
mineralco-download --source mineral_db --output ~/mineralco_data

# Download sample synchrotron data
mineralco-download --source synchrotron --mineral bridgmanite --output ~/mineralco_data

# Download all benchmark data (may take time)
mineralco-download --all --output ~/mineralco_data
```

Step 6: Test Installation

```bash
# Run diagnostic
mineralco-diagnostic --all

# Expected output:
# ✅ Python version: 3.10.x
# ✅ MINERALCO version: 1.0.0
# ✅ Core modules: installed
# ✅ NumPy: 1.24.x
# ✅ SciPy: 1.10.x
# ✅ Spglib: 2.0.x
# ✅ Data directories: found
# ✅ 47 minerals loaded
```

---

🐳 Docker Installation

Docker Compose (Full Stack)

```bash
# Clone repository
git clone https://github.com/gitedeeper9/mineralco.git
cd mineralco

# Set environment variables
export DB_PASSWORD=$(openssl rand -base64 32)

# Start all services
docker-compose up -d

# Access services:
# - Web Dashboard: http://localhost:5000
# - API: http://localhost:8000
```

---

📊 Quick Start Examples

Example 1: Calculate Bridgmanite EOS

```python
import mineralco as mc

# Load bridgmanite parameters
bridgmanite = mc.load_mineral('bridgmanite')

# Calculate pressure at given volume
P = mc.birch_murnaghan_3rd_order(
    V0=bridgmanite.V0,
    K0=bridgmanite.K0,
    Kprime=bridgmanite.Kprime,
    V=20.0  # cm³/mol
)
print(f"Pressure at V=20 cm³/mol: {P:.1f} GPa")

# Calculate volume at given pressure and temperature
V = mc.volume_at_PT(
    mineral='bridgmanite',
    P=50,  # GPa
    T=2000  # K
)
print(f"Volume at 50 GPa, 2000 K: {V:.2f} cm³/mol")
```

Example 2: Calculate CSI for Phase Transition

```python
import mineralco as mc

# Check ringwoodite stability near 660 km discontinuity
ringwoodite = mc.load_mineral('ringwoodite')
csi = mc.crystal_stability_index(
    mineral=ringwoodite,
    P=23.0,  # GPa (near 660 km)
    T=1900   # K
)
print(f"CSI at 23 GPa, 1900 K: {csi:.2f}")
if csi >= 0.85:
    print("⚠️ Phase transition imminent!")
```

Example 3: Batch Process Multiple Minerals

```bash
# Process all 47 benchmark minerals
mineralco-process --all --output ./results

# Generate report
mineralco-report --input ./results --format pdf
```

---

✅ Installation Verification

```bash
#!/bin/bash
# verify_installation.sh

echo "🔍 Verifying MINERALCO installation..."

# Check Python
python --version || exit 1

# Check package
pip show mineralco || exit 1

# Check version
python -c "import mineralco; print(f'Version: {mineralco.__version__}')"

# Check modules
python -c "
import mineralco.physics
import mineralco.data
import mineralco.visualization
print('✅ All modules imported successfully')
"

# Check data
python -c "
from mineralco.data import MineralDatabase
db = MineralDatabase()
print(f'✅ Loaded {len(db.minerals)} minerals')
"

# Run test calculation
python -c "
from mineralco.physics import BirchMurnaghanEOS
eos = BirchMurnaghanEOS(K0=260.7, Kprime=3.97, V0=24.45)
P = eos.pressure(V=20.0)
print(f'✅ Test calculation: P={P:.1f} GPa')
"

echo "✅ Installation verification complete!"
```

---

🚨 Troubleshooting

Common Issues

Issue: "Module not found" errors

```bash
# Solution: Reinstall with all dependencies
pip uninstall mineralco -y
pip install mineralco[all]
```

Issue: Spglib import error

```bash
# Solution: Install crystallography dependencies
pip install spglib pymatgen ase
```

Issue: Data download fails

```bash
# Solution: Use manual download
mineralco-download --source mineral_db --url https://mirror.example.com/mineral_db.json
```

Issue: Out of memory

```bash
# Solution: Reduce chunk size
mineralco-config set processing.chunk_size 100
```

Logs

```bash
# Check logs
tail -f ~/.mineralco/logs/mineralco.log

# Increase log level for debugging
mineralco-config set logging.level DEBUG
```

---

📚 Additional Resources

· Documentation: https://mineralco.netlify.app/docs
· API Reference: https://mineralco.netlify.app/api
· GitHub: https://github.com/gitedeeper9/mineralco
· PyPI: https://pypi.org/project/mineralco/
· Docker Hub: https://hub.docker.com/r/gitedeeper9/mineralco
· DOI: 10.5281/zenodo.19009597

---

📞 Support

For installation assistance:

· Email: gitdeeper@gmail.com
· GitHub Issues: https://github.com/gitedeeper9/mineralco/issues
· ORCID: 0009-0003-8903-0029

---

Version: 1.0.0
Last Updated: 2026-03-14
