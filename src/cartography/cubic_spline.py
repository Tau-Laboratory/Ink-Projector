from math import sqrt
from typing import List
import numpy as np

"""
This is a "manual" implementation of a cubic spline interpolator.
We use this instead of scipy as this may not be deployed with inkscape.
"""

class CubicSplineInterpolator():
    """
    Interpolate a 1-D function using cubic splines.
      x0 : a float or an 1d-array
      x : (N,) array_like
          A 1-D array of real/complex values.
      y : (N,) array_like
          A 1-D array of real values. The length of y along the
          interpolation axis must be equal to the length of x.

    Natural cubic spline interpolate function
    This function is licenced under: Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
    https://creativecommons.org/licenses/by-sa/3.0/
    Author raphael valentin
    Date 25 Mar 2022
    Link https://stackoverflow.com/a/71615189 
    """

    def __init__(self, x: List[float], y: List[float]) -> None:
        self.x = np.array(x)
        self.y = np.array(y)
        xdiff = np.diff(self.x)
        dydx = np.diff(self.y)
        dydx /= xdiff

        n = self.size = len(self.x)

        w = np.empty(n-1, float)
        self.z = np.empty(n, float)

        w[0] = 0.
        self.z[0] = 0.
        for i in range(1, n-1):
            m = xdiff[i-1] * (2 - w[i-1]) + 2 * xdiff[i]
            w[i] = xdiff[i] / m
            self.z[i] = (6*(dydx[i] - dydx[i-1]) - xdiff[i-1]*self.z[i-1]) / m
        self.z[-1] = 0.

        for i in range(n-2, -1, -1):
            self.z[i] = self.z[i] - w[i]*self.z[i+1]

    def evaluate(self, x0: float):
        return self.evaluate_list([x0])[0]    
    
    def evaluate_list(self, x0: List[float]):
        # find index (it requires x0 is already sorted)
        index = self.x.searchsorted(x0)
        np.clip(index, 1, self.size-1, index)

        xi1, xi0 = self.x[index], self.x[index-1]
        yi1, yi0 = self.y[index], self.y[index-1]
        zi1, zi0 = self.z[index], self.z[index-1]
        hi1 = xi1 - xi0

        # calculate cubic
        f0 = zi0/(6*hi1)*(xi1-x0)**3 + \
            zi1/(6*hi1)*(x0-xi0)**3 + \
            (yi1/hi1 - zi1*hi1/6)*(x0-xi0) + \
            (yi0/hi1 - zi0*hi1/6)*(xi1-x0)
        return f0