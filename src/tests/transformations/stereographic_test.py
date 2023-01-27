import unittest
from cartography.projection_types import Pole
from tests.transformations.transformation_field import TransformationField
from cartography.transformations.map_transformation import get_stereographic_projection
from tests.transformations.map_transform_test import MapTransformTest
from numpy import pi, floor

class StereographicTest(MapTransformTest):
    def test_bounds(self):
        latitude_limit = 0.0
        pole = Pole.NORTHPOLE
        transformation = get_stereographic_projection(200,100, latitude_limit, pole)
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

    def test_latitude_limit_poles(self):
        latitude_limit = 0.0
        pole = Pole.NORTHPOLE
        transformation = get_stereographic_projection(200,100, latitude_limit, pole)
        field = TransformationField(transformation, 21, 11)
        radii = field.get_horizontal_circle_radii((100, 50))

        for i in range(len(radii)):
            if i > 0 and i <= 5:
                self.assertGreater(radii[i], radii[i-1])
            if i>=5:
                # We have reached the Latitude Limit => All radii are clamped
                self.assertEqual(50, radii[i])
        
        latitude_limit = 0.0
        pole = Pole.SOUTHPOLE
        transformation = get_stereographic_projection(200,100, latitude_limit, pole)
        field = TransformationField(transformation, 21, 11)
        radii = field.get_horizontal_circle_radii((100, 50))

        for i in range(len(radii)):
            if i > 5:
                self.assertLess(radii[i], radii[i-1])
            if i<=5:
                # We have reached the Latitude Limit => All radii are clamped
                self.assertEqual(50, radii[i])
    
    def test_latitude_limits(self):
        limits = [-pi/3, 0.0, pi/4, pi/6]
        for limit in limits:
            cutoff = floor(((limit+pi/2) / pi) * 11)
            pole = Pole.NORTHPOLE
            transformation = get_stereographic_projection(200,100, limit, pole)
            field = TransformationField(transformation, 21, 11)
            radii = field.get_horizontal_circle_radii((100, 50))

            for i in range(len(radii)):
                if i > 0 and i <= cutoff:
                    self.assertGreater(radii[i], radii[i-1])
                if i > cutoff:
                    # We have reached the Latitude Limit => All radii are clamped
                    self.assertEqual(50, radii[i])

if __name__ == "__main__":
    unittest.main()