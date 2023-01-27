from cartography.transformations.generic_transformation import *
from tests.test_2D import Test2D
from numpy import linspace


class LinearTransformTest(Test2D):
    def test_transform(self):
        in_x_min, in_x_max = 0, 123.45
        in_y_min, in_y_max = -110, -5.2
        in_bound = ((in_x_min, in_y_min), (in_x_max, in_y_max))
        out_x_min, out_x_max = -20.1, 20.1
        out_y_min, out_y_max = 0, 1.0
        out_bound = ((out_x_min, out_y_min), (out_x_max, out_y_max))
        transform = get_linear_transform(in_bound, out_bound)
        resolution = 100

        x_points_in = linspace(in_x_min, in_x_max, resolution)
        y_points_in = linspace(in_y_min, in_y_max, resolution)
        x_points_out = linspace(out_x_min, out_x_max, resolution)
        y_points_out = linspace(out_y_min, out_y_max, resolution)

        for i in range(resolution):
            for j in range(resolution):
                point_in = (x_points_in[i], y_points_in[j])
                point_out = (x_points_out[i], y_points_out[j])
                self.assertPointEqual(point_out, transform(*point_in))

class CircleBoundTest(Test2D):
    def test_circle(self):
        bound = get_circle_bound(5.0, 4.2)
        self.assertEqual(((-5.0, -4.2),(5.0, 4.2)), bound)

class CenteredSquareTest(Test2D):
    def test_perfect_square(self):
        bound = get_centered_square_bound(10.0, 10.0)
        self.assertEqual(((0.0, 0.0),(10.0,10.0)), bound)

    def test_long_rectangle(self):
        bound = get_centered_square_bound(30.0, 10.0)
        self.assertEqual(((10.0, 0.0),(20.0,10.0)), bound)

    def test_high_rectange(self):
        actual_bound = get_centered_square_bound(5.2, 42.0)
        low, high = actual_bound
        xmin, ymin = low 
        xmax, ymax = high
        self.assertAlmostEqual(0.0, xmin)
        self.assertAlmostEqual(18.4, ymin)
        self.assertAlmostEqual(5.2, xmax)
        self.assertAlmostEqual(23.6, ymax)

class RectangleTest(Test2D):
    def test_rectangle(self):
        bound = get_rectangle_bound(10.0, 3.1)
        self.assertEqual(((0.0, 0.0),(10.0, 3.1)), bound)

class LongLatTest(Test2D):
    def test_long_lat(self):
        bound = get_long_lat_bound()
        self.assertEqual(((-pi, -pi/2),(pi, pi/2)), bound)

class TransformToFitTest(Test2D):
    def _get_new_bounds(self, old_bounds, transform):
        low, high = old_bounds
        new_low = transform(*low)
        new_high = transform(*high)
        return (new_low, new_high)

    def test_bound_change(self):
        pass
    
    def test_aspect_ratio(self):
        old_bounds = ((10.0, -40.0), (290.0, 70.0))
        low, high = old_bounds
        x_min, y_min = low
        x_max, y_max = high
        width = x_max - x_min
        height = y_max - y_min
        old_aspect_ratio = width / height
        transform = get_transform_to_fit(old_bounds, 400.0, 200.0)
        new_bounds = self._get_new_bounds(old_bounds, transform)
        low, high = new_bounds
        x_min, y_min = low
        x_max, y_max = high
        width = x_max - x_min
        height = y_max - y_min
        new_aspect_ratio = width / height
        self.assertAlmostEqual(old_aspect_ratio, new_aspect_ratio)



        