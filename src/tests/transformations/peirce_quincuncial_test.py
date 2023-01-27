import unittest
from cartography.projection_types import Point
from cartography.transformations.map_transformation import get_peirce_quincuncial_projection
from tests.transformations.transformation_field import TransformationField
from tests.transformations.map_transform_test import MapTransformTest

class PeirceQuincuncialTest(MapTransformTest):
    def test_bounds(self):
        transformation = get_peirce_quincuncial_projection(200, 100, 0.0)
        x_resolution = 25
        field = TransformationField(transformation, x_resolution, 11)
        # Test Aspect Ratio / bounds
        self.assertTrue(field.is_centered(200, 100))
        self.assertAlmostEqual(100, field.get_height())
        self.assertAlmostEqual(1.0, field.get_aspect_ratio())
        # Test Prallelism & monotonicity
        self.assertFalse(field.horizontals_parallel)
        self.assertFalse(field.verticals_parallel)
        self.assertFalse(field.horizontal_monotone)
        self.assertFalse(field.vertical_monotone)

        # Test Equator
        equator = [field.points[i][5] for i in range(x_resolution)]
        self.assertPointEqual(equator[0], equator[-1])
        equator = equator[:-1]
        equator = equator[-3:] + equator[:-2]

        # Lines  
        # 0->6      (100,100) -> ( 50, 50)
        for point in equator[0:7]:
            self.assertTrue(is_on_line((100,100), (50,50), point))
        # 6->12     ( 50, 50) -> (100,  0)
        for point in equator[6:13]:
            self.assertTrue(is_on_line((50,50), (100,0), point))
        # 12->18    (100,  0) -> (150, 50)
        for point in equator[12:19]:
            self.assertTrue(is_on_line((100,0), (150,50), point))
        # 18->24    (150, 50) -> (100,100) 
        for point in equator[18:25]:
            self.assertTrue(is_on_line((150,50), (100,100), point))

def is_on_line(start: Point, end: Point, test_point: Point, delta=0.0001) -> bool:
    start_x, start_y = start
    end_x, end_y = end
    delta_x, delta_y = end_x - start_x, end_y - start_y

    test_x, test_y = test_point
    test_delta_x, test_delta_y = test_x - start_x, test_y - start_y 

    x_index, y_index = test_delta_x / delta_x, test_delta_y / delta_y
    if abs(x_index - y_index) > delta:
        # Point is not on the line
        return False
    if x_index < (0.0-delta) or x_index > (1.0+delta):
        # Point outside the segment
        return False
    return True
    

if __name__ == "__main__":
    unittest.main()