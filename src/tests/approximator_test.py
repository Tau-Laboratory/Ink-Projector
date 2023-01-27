from tests.test_2D import Test2D
from cartography.approximator import get_equidistant_approximator
from numpy import pi, sin, cos, linspace
from cartography.projection_types import Point
from cartography.basis_function import get_line_function
from typing import List

class EquidistantApproximatorTest(Test2D):
    def test_simple_line(self):
        line = get_line_function((0,0), (100, -10))
        approximator = get_equidistant_approximator(0.1, 100, 1, 0.0, 0)
        points = approximator(line)
        self.assertEqual(2, len(points))
        self.assertPointEqual((0,0), points[0])
        self.assertPointEqual((100,-10), points[1])

    def test_max_point_count(self):
        circle = get_circle_function((0,0), 100)
        approximator = get_equidistant_approximator(0.1, 3, 1, 0.0, 0)
        points = approximator(circle)
        self.assertEqual(3, len(points))
        self.assertPointEqual((100,0), points[0])
        self.assertPointEqual((-100,0), points[1])
        self.assertPointEqual((100,0), points[2])

    def test_precision(self):
        circle = get_circle_function((0,0), 100)
        point_count = 5000
        approximator = get_equidistant_approximator(0.0001, point_count, 1, 0.0, 0)
        points = approximator(circle)
        approximated_circle = get_approximated_function(points)
        self.assertGreater(point_count, len(points))
        self.assertFunctionEqual(circle, approximated_circle, 0.0, 1.0, point_count+10, 3)

    def test_z_score(self):
        def jump_parabola(t: float) -> Point:
            scaled_t = 10*t
            if t < 0.5:
                return (scaled_t, scaled_t*scaled_t)
            return (scaled_t, scaled_t*scaled_t+10)
        approximator = get_equidistant_approximator(0.001, 40, 1, 3.0, 5)
        points = approximator(jump_parabola)
        self.assertEqual(45, len(points))

        # The Jump happens around t=0.5 so point 19 -> point 20
        # should be z-filled
        jump_position = 20
        # Check that everything without the zfill is evenly distributed
        regular_points = points[:jump_position] + points[jump_position+5:]
        self.assertEqual(40, len(regular_points))
        x_points = linspace(0.0, 10.0, 40)
        for i in range(len(regular_points)):
            self.assertAlmostEqual(x_points[i], regular_points[i][0])

        # Check the distribution of the zfill
        low_bound, _ = points[jump_position-1]
        high_bound, _ = points[jump_position+5]
        fill_size = (high_bound - low_bound) / 6
        zfill = points[jump_position:jump_position+5]
        self.assertEqual(5, len(zfill))
        for i, fill_point in enumerate(zfill):
            x,_ = fill_point
            self.assertAlmostEqual(low_bound + (i+1)*fill_size, x)


def get_circle_function(center: Point, radius: float):
    center_x, center_y = center
    tau = 2* pi
    def circle(t: float) -> Point:
        angle = tau * t
        x = center_x + radius * cos(angle)
        y = center_y + radius * sin(angle)
        return x,y
    return circle

def get_approximated_function(point_list: List[Point]):
    segment_count = len(point_list) - 1 
    segment_length = 1.0 / segment_count
    def function(t: float) -> Point:
        if t == 1.0:
            return point_list[-1]

        segment_index, segment_position  = divmod(t,  segment_length)
        start_x, start_y = point_list[int(segment_index)]
        end_x, end_y = point_list[int(segment_index)+1]
        
        dx = (end_x - start_x)/ segment_length
        dy = (end_y - start_y)/ segment_length
        x = start_x + dx*segment_position
        y = start_y + dy*segment_position
        return x,y 

        
    return function