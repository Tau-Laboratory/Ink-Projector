import unittest
from tests.transformations.transformation_field import TransformationField
from cartography.transformations.map_transformation import get_equidistant_conic_projection
from tests.transformations.map_transform_test import MapTransformTest
from numpy import pi

class EquidistantConicTest(MapTransformTest):
    def test_bounds(self):
        standard_a, standard_b = pi/3, pi*2/3
        transformation = get_equidistant_conic_projection(200, 100, 0.0, 0.0, standard_a, standard_b)
        field = TransformationField(transformation, 21, 11)
        # Test bounds
        self.assertTrue(field.is_centered(200, 100))
        self.assertAlmostEqual(100, field.get_height())
        # Test Prallelism & monotonicity
        self.assertFalse(field.horizontals_parallel)
        self.assertFalse(field.verticals_parallel)
        self.assertFalse(field.horizontal_monotone)
        self.assertFalse(field.vertical_monotone)
    
    def test_equidistance(self):
        standard_a, standard_b = 0.0, 0.0
        transformation = get_equidistant_conic_projection(200, 100, 0.0, 0.0, standard_a, standard_b)
        field = TransformationField(transformation, 21, 11)
        # Test Aspect Ratio / bounds
        self.assertTrue(field.is_centered(200, 100))
        aspect_ratio = 2.0
        self.assertAlmostEqual(100, field.get_height())
        self.assertAlmostEqual(aspect_ratio, field.get_aspect_ratio())
        for i in range(len(field.points)):
            for j in range(len(field.points[i])):
                self.assertPointEqual((10*i, 10*j), field.points[i][j])

        standard_a, standard_b = -1.0, 1.0
        transformation = get_equidistant_conic_projection(200, 100, 0.0, 0.0, standard_a, standard_b)
        field = TransformationField(transformation, 21, 11)
        # Test Aspect Ratio / bounds
        self.assertTrue(field.is_centered(200, 100))
        aspect_ratio = 2.0
        self.assertAlmostEqual(100, field.get_height())
        self.assertAlmostEqual(aspect_ratio, field.get_aspect_ratio())
        for i in range(len(field.points)):
            for j in range(len(field.points[i])):
                self.assertPointEqual((10*i, 10*j), field.points[i][j])



if __name__ == "__main__":
    unittest.main()