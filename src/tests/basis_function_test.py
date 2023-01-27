import unittest
from cartography.basis_function import *
from tests.test_2D import Test2D 

class TestLineFunction(Test2D):
    def test_line_simple(self):
        line = get_line_function((0,0), (2,2))
        self.assertPointEqual((0.0, 0.0), line(0.0))
        self.assertPointEqual((1.0, 1.0), line(0.5))
        self.assertPointEqual((2.0, 2.0), line(1.0))

    def test_line_negative(self):
        line = get_line_function((1, -1), ( -4, 0.5))
        self.assertPointEqual((1.0, -1.0), line(0.0))
        self.assertPointEqual((-1.5, -0.25), line(0.5))
        self.assertPointEqual((-4.0, 0.5), line(1.0))

    def test_line_zero_delta(self):
        line = get_line_function((-10, 2), ( -10, 2))
        self.assertPointEqual((-10, 2), line(0.0))
        self.assertPointEqual((-10, 2), line(0.5))
        self.assertPointEqual((-10, 2), line(1.0))

    def test_line_out_of_bounds(self):
        line = get_line_function((1.0, 1.0), (0.0, 0.0))
        self.assertPointEqual((2.0, 2.0), line(-1.0))
        self.assertPointEqual((-1.0, -1.0), line(2.0))

class TestQuadraticBezierFunction(Test2D):
    def test_quadratic_simple(self):
        quadratic = get_quadratic_bezier_function((0,0), (1, 1), (2,0))
        self.assertPointEqual((0.0, 0.0), quadratic(0.0))
        self.assertPointEqual((2/3, 4/9), quadratic(1/3))
        self.assertPointEqual((1.0, 0.5), quadratic(0.5))
        self.assertPointEqual((4/3, 4/9), quadratic(2/3))
        self.assertPointEqual((2.0, 0.0), quadratic(1.0))
    

class TestCubicBezierFunction(Test2D):
    def test_cubic_simple(self):
        cubic = get_cubic_bezier_function((0,0), (0,2), (2,2), (2,0))
        self.assertPointEqual((0.0,      0.0), cubic(0.0))
        self.assertPointEqual((0.3125, 1.125), cubic(0.25))
        self.assertPointEqual((1.0,      1.5), cubic(0.5))
        self.assertPointEqual((1.6875, 1.125), cubic(0.75))
        self.assertPointEqual((2.0,      0.0), cubic(1.0))

class TestArcFunction(Test2D):
    def _get_test_arc(self, large_arc: bool, sweep: bool):
        return get_arc_function((0,0), (5,5), (5,5), 0, large_arc, sweep)

    def assert_is_circle(self, test_arc, center: Point, radius: float, start_angle: float, end_angle: float):
        angle_size = end_angle - start_angle
        def test_circle(t):
            angle = start_angle + t* angle_size
            x = center[0] + radius * cos(angle)
            y = center[1] + radius * sin(angle)
            return x,y
        
        self.assertFunctionEqual(test_circle, test_arc, 0.0, 1.0, 100)

    def test_arc_simple(self):
        arc = self._get_test_arc(False, False)
        # center (5,0) from angle pi to pi/2
        self.assert_is_circle(arc, (5,0), 5, pi, pi/2)

    def test_arc_sweep(self):
        arc = self._get_test_arc(False, True)
        # center (0,5) from angle 3*pi/2 to 2*pi
        self.assert_is_circle(arc, (0,5), 5, 3*pi/2, 2*pi)

    def test_arc_large(self):
        arc = self._get_test_arc(True, False)
        # center (0,5) from angle pi to 5*pi/2
        self.assert_is_circle(arc, (0,5), 5, 3*pi/2, 0)

    def test_arc_large_sweep(self):
        arc = self._get_test_arc(True, True)
        # center (5,0) from angle 3*pi/2 to 0
        self.assert_is_circle(arc, (5,0), 5, pi, 5*pi/2)

class TestClampFunction(Test2D):
    def test_clamp(self):
        clamp = get_clamp( ((-1, -1),(1, 1)) )
        self.assertPointEqual((-1.0, -1.0), clamp(-10, -4))
        self.assertPointEqual((-0.2, 0.5), clamp(-0.2, 0.5))
        self.assertPointEqual((-0.6, 1.0), clamp(-0.6, 1.5))
        self.assertPointEqual((1.0, 1.0), clamp(3, 1.5))
        


if __name__ == '__main__':
    unittest.main()