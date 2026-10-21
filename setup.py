from setuptools import find_packages, setup

setup(
    name="artemis-surf",
    version="1.0.0",
    description="ArtemisSurf - a minimal, transparent, privacy-first web browser",
    packages=find_packages(),
    install_requires=["PyQt6>=6.6", "PyQt6-WebEngine>=6.6"],
    entry_points={"console_scripts": ["artemissurf=artemis.app:run"]},
    python_requires=">=3.9",
)
