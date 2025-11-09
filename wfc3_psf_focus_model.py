"""
Simple focus model utilities.

This module provides a lightweight class to model PSF focus changes from images.
The implementation is intentionally simple and meant as a starting point to
be replaced/extended with instrument-specific modeling later.
"""

from typing import Sequence, Tuple
import numpy as np
from scipy.optimize import least_squares


class FocusModel:
    """
    Fit a simple focus metric model to a set of PSF images.

    The model here is deliberately minimal:
    - A scalar focus parameter f for each image
    - A Gaussian model for how the PSF second-moment (or other metric) depends on focus

    Methods:
    - fit_focus_metrics: estimate focus values given metrics and times
    - predict_metric: predict metric for a given focus value
    """

    def __init__(self):
        self.fitted = False
        self.params = {}

    @staticmethod
    def metric_from_image(image: np.ndarray) -> float:
        """
        Compute a simple metric from a PSF image. Default: second moment (size).

        Args:
            image: 2D array

        Returns:
            float metric
        """
        image = np.asarray(image, dtype=float)
        total = image.sum()
        if total <= 0:
            return 0.0
        ys, xs = np.indices(image.shape)
        xcen = (xs * image).sum() / total
        ycen = (ys * image).sum() / total
        dx2 = ((xs - xcen) ** 2 * image).sum() / total
        dy2 = ((ys - ycen) ** 2 * image).sum() / total
        return float(np.sqrt(dx2 + dy2))

    @staticmethod
    def gaussian_model(f, a, f0, sigma, c):
        """a * exp(-0.5*((f-f0)/sigma)^2) + c"""
        return a * np.exp(-0.5 * ((f - f0) / sigma) ** 2) + c

    def fit_focus_metrics(self, times: Sequence[float], metrics: Sequence[float], initial_guess=(1.0, 0.0, 1.0, 0.0)):
        """
        Fit a 1D Gaussian model of the metric vs focus parameter (here times are a proxy).

        Args:
            times: 1D sequence (e.g. observation times or arbitrary index)
            metrics: measured metric per time
            initial_guess: (a, f0, sigma, c)
        """
        times = np.asarray(times, dtype=float)
        metrics = np.asarray(metrics, dtype=float)

        def residuals(p):
            a, f0, sigma, c = p
            pred = self.gaussian_model(times, a, f0, sigma, c)
            return pred - metrics

        res = least_squares(residuals, x0=np.array(initial_guess))
        self.params = {
            "a": float(res.x[0]),
            "f0": float(res.x[1]),
            "sigma": float(abs(res.x[2])),
            "c": float(res.x[3]),
            "cost": float(res.cost),
            "success": bool(res.success),
        }
        self.fitted = True
        return self.params

    def predict_metric(self, times: Sequence[float]) -> np.ndarray:
        """
        Predict metric for provided times using the fitted model.

        Raises:
            RuntimeError if model not yet fitted.
        """
        if not self.fitted:
            raise RuntimeError("FocusModel is not fitted yet.")
        times = np.asarray(times, dtype=float)
        p = self.params
        return self.gaussian_model(times, p["a"], p["f0"], p["sigma"], p["c"])