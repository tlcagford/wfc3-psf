from wfc3_psf import models, fitting

# Create a theoretical PSF model
psf_model = models.create_psf_model(detector='UVIS', filter='F606W')

# Fit observed stellar profile
result = fitting.fit_psf(star_data, psf_model)