"""
Simple anomaly detection for PSF metrics.

This module implements a robust sigma-clipping based detector that flags outliers
in a 1D metric time series. It is intentionally lightweight so it can be used
as a building block for more complex detectors.
"""

from typing import Sequence, Tuple
import numpy as np


class AnomalyDetector:
    """
    Detect anomalies in a 1D metric series.

    Methods:
    - detect_anomalies: returns boolean mask of anomalies
    - anomaly_indices: convenience to return integer indices
    """

    @staticmethod
    def detect_anomalies(metrics: Sequence[float], threshold_sigma: float = 5.0, window: int = 1) -> np.ndarray:
        """
        Detect anomalies by comparing each point to a robust estimate of the local median and MAD.

        Args:
            metrics: 1D sequence of metric values
            threshold_sigma: how many sigma (where sigma ~ 1.4826*MAD) to flag
            window: integer radius for local stats (0 => global)

        Returns:
            boolean numpy array (True = anomaly)
        """
        y = np.asarray(metrics, dtype=float)
        n = y.size
        mask = np.zeros(n, dtype=bool)

        if n == 0:
            return mask

        if window <= 0:
            med = np.median(y)
            mad = np.median(np.abs(y - med))
            sigma = 1.4826 * mad if mad > 0 else np.std(y)
            if sigma == 0:
                return mask
            mask = np.abs(y - med) > threshold_sigma * sigma
            return mask

        # local windowing
        for i in range(n):
            lo = max(0, i - window)
            hi = min(n, i + window + 1)
            seg = y[lo:hi]
            med = np.median(seg)
            mad = np.median(np.abs(seg - med))
            sigma = 1.4826 * mad if mad > 0 else np.std(seg)
            if sigma == 0:
                continue
            if abs(y[i] - med) > threshold_sigma * sigma:
                mask[i] = True
        return mask

    @staticmethod
    def anomaly_indices(metrics: Sequence[float], threshold_sigma: float = 5.0, window: int = 1) -> Tuple[int, ...]:
        mask = AnomalyDetector.detect_anomalies(metrics, threshold_sigma=threshold_sigma, window=window)
        return tuple(int(i) for i in np.nonzero(mask)[0])