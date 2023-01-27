import unittest
from cartography.transformations.map_transformation import get_robinson_projection
from tests.transformations.transformation_field import TransformationField
from tests.transformations.map_transform_test import MapTransformTest
import numpy as np

class RobinsonTest(MapTransformTest):
    def test_bounds(self):
        transformation = get_robinson_projection(200,100, 0.0)
        field = TransformationField(transformation, 21, 11)
        self.assertTrue(field.is_centered(200, 100))

        aspect_ratio = 0.8487 * np.pi / 1.3523
        self.assertAlmostEqual(100, field.get_height())
        self.assertAlmostEqual(aspect_ratio, field.get_aspect_ratio())

        # Test Prallelism & monotonicity
        self.assertTrue(field.horizontal_monotone)
        self.assertTrue(field.vertical_monotone)

        for i in range(len(field.points)):
            for j in range(len(field.points[i])):
                _, y = field.points[i][j]
                if i > 0:
                    _, y_prev = field.points[i-1][j]
                    self.assertAlmostEqual(y_prev, y)

if __name__ == "__main__":
    unittest.main()