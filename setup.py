from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wfc3-psf",
    version="0.1.0",
    author="tlcagford",
    author_email="YOUR_EMAIL@example.com",
    description="PSF modeling and analysis tools for Hubble WFC3 instrument",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tlcagford/wfc3-psf",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "scipy>=1.6.0",
        "matplotlib>=3.3.0",
        "astropy>=4.2.0",
        "photutils>=1.0.0",
    ],
)