import unittest
from tests.transformations.transformation_field import TransformationField
from cartography.transformations.map_transformation import get_cylindrical_equal_area_projection
from tests.transformations.map_transform_test import MapTransformTest
import numpy as np

class CylindricalEqualAreaTest(MapTransformTest):
    def test_bounds(self):
        standard_latitude = 0.0
        transformation = get_cylindrical_equal_area_projection(200, 100, 0.0, standard_latitude)
        field = TransformationField(transformation, 20, 10)
        # Test Aspect Ratio / bounds
        self.assertTrue(field.is_centered(200, 100))
        self.assertAlmostEqual(200, field.get_width())
        aspect_ratio = np.pi * (np.cos(standard_latitude)**2)
        self.assertAlmostEqual(aspect_ratio, field.get_aspect_ratio())
        # Test Prallelism & monotonicity
        self.assertTrue(field.horizontals_parallel)
        self.assertTrue(field.verticals_parallel)
        self.assertTrue(field.horizontal_monotone)
        self.assertTrue(field.vertical_monotone)

    def test_standard_latitudes(self):
        # Test Aspect Ratio
        for standard_latitude in [np.pi*0.1, np.pi*0.25, np.pi/3, np.pi*0.5]:
            transformation = get_cylindrical_equal_area_projection(200, 100, 0.0, standard_latitude)
            field = TransformationField(transformation, 20, 10)
            aspect_ratio = np.pi * (np.cos(standard_latitude)**2)
            self.assertAlmostEqual(aspect_ratio, field.get_aspect_ratio())


if __name__ == "__main__":
    unittest.main()