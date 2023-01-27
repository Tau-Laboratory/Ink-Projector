import unittest
from cartography.projection_types import Pole
from tests.transformations.transformation_field import TransformationField
from cartography.transformations.map_transformation import get_orthographic_projection
from tests.transformations.map_transform_test import MapTransformTest
from numpy import pi, floor

class OrthographicTest(MapTransformTest):
    def test_bounds(self):
        origin = (0.0, -pi/2)
        transformation = get_orthographic_projection(200,100, origin)
        field = TransformationField(transformation, 21, 11)
        self.assertTrue(field.is_centered(200, 100))

        aspect_ratio = 1.0
        self.assertAlmostEqual(100, field.get_height())
        self.assertAlmostEqual(aspect_ratio, field.get_aspect_ratio())

        # Test Prallelism & monotonicity
        self.assertFalse(field.horizontals_parallel)
        self.assertFalse(field.verticals_parallel)
        self.assertFalse(field.horizontal_monotone)
        self.assertFalse(field.vertical_monotone)
        # Parallels are transformed to circles around (100,50)
        self.assertTrue(field.has_horizontal_circles((100,50)))

    def test_origin_poles(self):
        origin = (0.0, -pi/2)
        transformation = get_orthographic_projection(200,100, origin)
        field = TransformationField(transformation, 21, 11)
        radii = field.get_horizontal_circle_radii((100, 50))

        for i in range(len(radii)):
            if i > 0 and i <= 5:
                self.assertGreater(radii[i], radii[i-1])
            if i>=5:
                # We have reached the Latitude Limit => All radii are clamped
                self.assertEqual(50, radii[i])
        
        origin = (0.0, pi/2)
        transformation = get_orthographic_projection(200,100, origin)
        field = TransformationField(transformation, 21, 11)
        radii = field.get_horizontal_circle_radii((100, 50))

        for i in range(len(radii)):
            if i > 5:
                self.assertLess(radii[i], radii[i-1])
            if i<=5:
                # We have reached the Latitude Limit => All radii are clamped
                self.assertEqual(50, radii[i])
    
    def test_origin_non_poles(self):
        origin = (0.0, 0.0)
        transformation = get_orthographic_projection(200,100, origin)
        field = TransformationField(transformation, 21, 11)
        # Center
        self.assertPointEqual((100,50), field.points[10][5])

        # Cornors
        cornor_a = field.points[0][0]
        cornor_b = field.points[20][0]
        cornor_c = field.points[0][10]
        cornor_d = field.points[20][10]
        points = [cornor_a, cornor_b, cornor_c, cornor_d]
        for x,y in points:
            radius = ((100-x)**2 + (50-y)**2) ** (1/2)
            self.assertAlmostEqual(50, radius)

if __name__ == "__main__":
    unittest.main()