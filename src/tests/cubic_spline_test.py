import unittest
from cartography.cubic_spline import CubicSplineInterpolator
from scipy.interpolate import CubicSpline
import numpy as np


class CubicSplineTest(unittest.TestCase):
    """
    Tests that the manual implementation of the cubic spline matches the scipy interpolation.
    """

    def test_interpolator(self):
        x_values = [-0.6,  0.0,  0.5, 1.0, 1.3]
        y_values = [ 0.0,  4.0, -0.1, 0.0, 3.5]

        scipi_spline = CubicSpline(x_values, y_values, bc_type='natural')
        interpolator = CubicSplineInterpolator(x_values, y_values)
        
        testpoints = np.linspace(-0.6, 1.3, 100)

        for x in testpoints:
            y_scipy = scipi_spline(x)
            y_interpolator = interpolator.evaluate(x)
            self.assertAlmostEqual(y_scipy, y_interpolator)

if __name__ == '__main__':
    unittest.main()