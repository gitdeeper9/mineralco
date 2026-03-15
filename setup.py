#!/usr/bin/env python3
# MINERALCO Setup Script
# Mineral Intelligence Network for Equation-of-state Research, Atomic Lattice COmputation
# Version: 1.0.0 | DOI: 10.5281/zenodo.19009597

import os
import sys
from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Read version
version = "1.0.0"

setup(
    name="mineralco",
    version=version,
    author="Samir Baladi",
    author_email="gitdeeper@gmail.com",
    description="MINERALCO: Seven Parameters to Decode the Earth's Solid Interior",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitedeeper9/mineralco",
    project_urls={
        "Documentation": "https://mineralco.netlify.app/docs",
        "Source": "https://github.com/gitedeeper9/mineralco",
        "Bug Reports": "https://github.com/gitedeeper9/mineralco/issues",
        "Discussion": "https://github.com/gitedeeper9/mineralco/discussions",
        "DOI": "https://doi.org/10.5281/zenodo.19009597",
        "Web Dashboard": "https://mineralco.netlify.app",
    },
    packages=find_packages(include=["mineralco", "mineralco.*"]),
    install_requires=requirements,
    python_requires=">=3.9, <3.12",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Geology",
    ],
    keywords="mineral-physics equation-of-state crystallography high-pressure mantle birch-murnaghan",
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "mineralco=mineralco.cli.main:cli",
            "mineralco-init=mineralco.cli.init:main",
            "mineralco-download=mineralco.cli.download:main",
            "mineralco-process=mineralco.cli.process:main",
            "mineralco-csi=mineralco.cli.csi:main",
            "mineralco-serve=mineralco.cli.serve:main",
            "mineralco-diagnostic=mineralco.cli.diagnostic:main",
            "mineralco-validate=mineralco.cli.validate:main",
            "mineralco-report=mineralco.cli.report:main",
            "mineralco-plot=mineralco.cli.plot:main",
            "mineralco-config=mineralco.cli.config:main",
        ],
        "mineralco.physics": [
            "bm3_eos = mineralco.physics.bm3:BirchMurnaghanEOS",
            "mie_gruneisen = mineralco.physics.mie_gruneisen:MieGruneisenCorrection",
            "crystal_symmetry = mineralco.physics.symmetry:CrystalSymmetry",
            "gruneisen = mineralco.physics.gruneisen:GruneisenParameter",
            "thermal_expansion = mineralco.physics.thermal:ThermalExpansion",
            "lattice_energy = mineralco.physics.lattice:BornLandeEnergy",
            "csi = mineralco.physics.csi:CrystalStabilityIndex",
        ],
        "mineralco.data": [
            "mineral_db = mineralco.data.loaders.mineral_db:MineralDatabaseLoader",
            "synchrotron = mineralco.data.loaders.synchrotron:SynchrotronDataLoader",
            "dac = mineralco.data.loaders.dac:DACDataLoader",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
        ],
        "web": [
            "flask>=2.3.0",
            "dash>=2.9.0",
            "gunicorn>=20.1.0",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "sphinx>=7.0.0",
            "flask>=2.3.0",
            "dash>=2.9.0",
        ],
    },
    platforms=["any"],
    license="MIT",
)

print("✅ MINERALCO setup complete!")
print(f"📦 Version: {version}")
print("📚 Documentation: https://mineralco.netlify.app/docs")
print("🐍 Python: >=3.9, <3.12")
