"""
Basic usage example for WFC3 PSF modeling
"""

import numpy as np
import matplotlib.pyplot as plt
from wfc3_psf import models

def demonstrate_basic_usage():
    """Demonstrate basic PSF modeling functionality"""
    
    print("WFC3 PSF Modeling Toolkit - Basic Usage Example")
    print("=" * 50)
    
    # Create PSF models for different detectors
    print("\n1. Creating PSF models:")
    uvis_psf = models.create_psf_model(detector='UVIS', filter='F606W')
    ir_psf = models.create_psf_model(detector='IR', filter='F160W')
    print(f"   UVIS F606W PSF model: {uvis_psf}")
    print(f"   IR F160W PSF model: {ir_psf}")
    
    # Generate a sample PSF
    print("\n2. Generating sample PSF:")
    psf_data = models.generate_sample_psf(size=51, fwhm=2.5)
    print(f"   Sample PSF shape: {psf_data.shape}")
    
    # Create visualization
    print("\n3. Creating visualization...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    im = ax1.imshow(psf_data, cmap='viridis', origin='lower')
    plt.colorbar(im, ax=ax1, label='Intensity')
    ax1.set_title('Sample PSF')
    
    profile = psf_data[25, :]  # Central row
    ax2.plot(profile)
    ax2.set_title('PSF Cross-section')
    ax2.set_xlabel('Pixel')
    ax2.set_ylabel('Intensity')
    
    plt.tight_layout()
    plt.savefig('examples/psf_demonstration.png', dpi=150, bbox_inches='tight')
    print("   Visualization saved as 'examples/psf_demonstration.png'")
    
    print("\nBasic usage demonstration completed!")

if __name__ == "__main__":
    demonstrate_basic_usage()