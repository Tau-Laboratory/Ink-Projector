import unittest
from tests.transformations.map_transform_test import MapTransformTest
from cartography.projection_types import Pole
from tests.transformations.transformation_field import TransformationField
from cartography.transformations.map_transformation import get_lambert_azimuthal_equal_area_projection
from numpy import pi, floor

class LambertAzimuthalEqualAreaTest(MapTransformTest):
    def test_bounds(self):
        pole = Pole.NORTHPOLE
        transformation = get_lambert_azimuthal_equal_area_projection(200,100, pole)
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
        pole = Pole.NORTHPOLE
        transformation = get_lambert_azimuthal_equal_area_projection(200,100, pole)
        field = TransformationField(transformation, 21, 11)
        radii = field.get_horizontal_circle_radii((100, 50))

        for i in range(len(radii)):
            if i > 0:
                self.assertGreater(radii[i], radii[i-1])
    
        pole = Pole.SOUTHPOLE
        transformation = get_lambert_azimuthal_equal_area_projection(200,100, pole)
        field = TransformationField(transformation, 21, 11)
        radii = field.get_horizontal_circle_radii((100, 50))

        for i in range(len(radii)):
            if i > 0:
                self.assertLess(radii[i], radii[i-1])

if __name__ == "__main__":
    unittest.main()