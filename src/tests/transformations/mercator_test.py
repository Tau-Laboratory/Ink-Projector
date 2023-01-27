import unittest
from cartography.transformations.map_transformation import get_mercator_projection
from tests.transformations.transformation_field import TransformationField
from tests.transformations.map_transform_test import MapTransformTest
import numpy as np

class MercatorTest(MapTransformTest):
    def test_bounds(self):
        cutoff = np.pi*0.40
        transformation = get_mercator_projection(200, 100, 0.0, cutoff)
        field = TransformationField(transformation, 20, 10)
        # Test Aspect Ratio / bounds
        self.assertTrue(field.is_centered(200, 100))
        aspect_ratio = np.pi / np.log(np.tan(np.pi/4 + cutoff/2))
        self.assertAlmostEqual(100, field.get_height())
        self.assertAlmostEqual(aspect_ratio, field.get_aspect_ratio())
        # Test Prallelism & monotonicity
        self.assertTrue(field.horizontals_parallel)
        self.assertTrue(field.verticals_parallel)
        self.assertTrue(field.horizontal_monotone)
        self.assertTrue(field.vertical_monotone)
    
    def test_cutoffs(self):
        cutoff = np.pi*0.40
        transformation = get_mercator_projection(200, 100, 0.0, cutoff)
        field_a = TransformationField(transformation, 20, 10)

        cutoff = np.pi*0.49
        transformation = get_mercator_projection(200, 100, 0.0, cutoff)
        field_b = TransformationField(transformation, 20, 10)

        cutoff = np.pi*0.499
        transformation = get_mercator_projection(200, 100, 0.0, cutoff)
        field_c = TransformationField(transformation, 20, 10)

        self.assertGreater(field_a.get_aspect_ratio(), field_b.get_aspect_ratio())
        self.assertGreater(field_b.get_aspect_ratio(), field_c.get_aspect_ratio())

if __name__ == "__main__":
    unittest.main()