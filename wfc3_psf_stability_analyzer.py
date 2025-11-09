"""
Stability analysis utilities.

Provides simple methods to quantify drift and stability in a time series of PSF metrics.
"""

from typing import Tuple, Sequence
import numpy as np


class StabilityAnalyzer:
    """
    Analyze stability of PSF metrics over time.

    Public methods:
    - compute_drift: linear slope of metric vs time
    - rolling_rms: compute rolling RMS of metric residuals
    - summary: quick summary stats
    """

    @staticmethod
    def compute_drift(times: Sequence[float], metrics: Sequence[float]) -> Tuple[float, float]:
        """
        Fit a straight line metric = m * time + b and return slope m and intercept b.
        Uses simple least squares.

        Returns:
            (slope, intercept)
        """
        t = np.asarray(times, dtype=float)
        y = np.asarray(metrics, dtype=float)
        if t.size < 2:
            return 0.0, float(y[0]) if t.size == 1 else (0.0, 0.0)
        A = np.vstack([t, np.ones_like(t)]).T
        m, b = np.linalg.lstsq(A, y, rcond=None)[0]
        return float(m), float(b)

    @staticmethod
    def rolling_rms(times: Sequence[float], metrics: Sequence[float], window: int = 5) -> np.ndarray:
        """
        Compute a rolling RMS of the residuals after detrending with a linear fit.

        Args:
            times, metrics: 1D sequences
            window: integer window size (must be >=1)

        Returns:
            rms array of same length as inputs (edges padded with nan to keep size)
        """
        t = np.asarray(times, dtype=float)
        y = np.asarray(metrics, dtype=float)
        if len(y) == 0:
            return np.array([])
        m, b = StabilityAnalyzer.compute_drift(t, y)
        resid = y - (m * t + b)

        if window <= 1:
            return np.sqrt(resid ** 2)

        rms = np.full_like(resid, np.nan, dtype=float)
        half = window // 2
        n = len(resid)
        for i in range(n):
            lo = max(0, i - half)
            hi = min(n, i + half + 1)
            seg = resid[lo:hi]
            if seg.size > 0:
                rms[i] = float(np.sqrt(np.mean(seg ** 2)))
        return rms

    @staticmethod
    def summary(times: Sequence[float], metrics: Sequence[float], window: int = 5) -> dict:
        """
        Quick summary including drift, median, std, and max RMS.

        Returns:
            dict with keys: slope, intercept, median, std, max_rms
        """
        t = np.asarray(times, dtype=float)
        y = np.asarray(metrics, dtype=float)
        slope, intercept = StabilityAnalyzer.compute_drift(t, y)
        rms = StabilityAnalyzer.rolling_rms(t, y, window=window)
        return {
            "slope": slope,
            "intercept": intercept,
            "median": float(np.nanmedian(y)),
            "std": float(np.nanstd(y)),
            "max_rms": float(np.nanmax(rms)) if rms.size > 0 else 0.0,
        }