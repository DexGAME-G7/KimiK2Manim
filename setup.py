"""Setup script for KimiK2Manim package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

setup(
    name="kimik2manim",
    version="0.1.0",
    description="Kimi K2 thinking model integration for Manim animation generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="HarleyCoops",
    url="https://github.com/HarleyCoops/KimiK2Manim",
    # Package structure: files are at root level
    py_modules=[
        "kimi_client",
        "tool_adapter", 
        "config",
    ],
    packages=["agents"],
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="kimi k2 moonshot ai manim animation mathematics physics",
)

