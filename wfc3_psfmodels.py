"""
PSF model definitions for WFC3
"""

import numpy as np
from astropy.modeling import models as astropy_models

def create_psf_model(detector='UVIS', filter=None, fwhm=None):
    """
    Create a PSF model for WFC3 detector.
    
    Parameters
    ----------
    detector : str
        Detector type: 'UVIS' or 'IR'
    filter : str, optional
        Filter name (e.g., 'F606W', 'F160W')
    fwhm : float, optional
        Full Width at Half Maximum in pixels
    
    Returns
    -------
    model : astropy.modeling.Fittable2DModel
        PSF model instance
    """
    
    # Set default FWHM based on detector and filter
    if fwhm is None:
        if detector == 'UVIS':
            fwhm = 2.0  # pixels, typical for UVIS
        else:  # IR
            fwhm = 1.5  # pixels, typical for IR
    
    # Create a 2D Gaussian as a simple PSF model
    psf_model = astropy_models.Gaussian2D(
        amplitude=1.0,
        x_mean=0,
        y_mean=0,
        x_stddev=fwhm / 2.355,  # Convert FWHM to sigma
        y_stddev=fwhm / 2.355,
    )
    
    return psf_model

def generate_sample_psf(size=51, fwhm=2.5):
    """
    Generate a sample PSF image.
    
    Parameters
    ----------
    size : int
        Size of the output array (size x size)
    fwhm : float
        Full Width at Half Maximum in pixels
    
    Returns
    -------
    psf : numpy.ndarray
        2D array containing the PSF
    """
    # Create coordinate grid
    y, x = np.mgrid[-size//2:size//2+1, -size//2:size//2+1]
    
    # Create Gaussian PSF
    sigma = fwhm / 2.355
    psf = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    # Normalize
    psf /= psf.sum()
    
    return psf