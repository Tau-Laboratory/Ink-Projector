import unittest
from cartography.projection_types import Point, Producer
import numpy as np


class Test2D(unittest.TestCase):
    """
    Base Class for many unittests.
    Contains some asserts for better reuse.
    """ 
    def assertPointEqual(self, first: Point, second: Point, places=7):
        """
        Asserts that two points are (almost) equal up to a given number of places.
        """
        self.assertAlmostEqual(first[0], second[0], places)
        self.assertAlmostEqual(first[1], second[1], places)

    def assertFunctionEqual(self, first: Producer, second: Producer, start: float, end: float, resolution: int, places=7):
        """
        Asserts that two producer functions yield the same results within the provided [start, end] interval.
        The test is done by sampling a given number of points form this interval.
        """
        test_points = np.linspace(start, end, resolution)
        for t in test_points:
            first_point = first(t)
            second_point = second(t)
            self.assertPointEqual(first_point, second_point, places)