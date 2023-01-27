import unittest
from cartography.transformations.map_transformation import get_winkel_tripel_projection
from tests.transformations.map_transform_test import MapTransformTest
from tests.transformations.transformation_field import TransformationField
import numpy as np

class WinkelTripelTest(MapTransformTest):
    def test_bounds(self):
        standard_parallel = 0.0 
        transformation = get_winkel_tripel_projection(200,100, standard_parallel)
        field = TransformationField(transformation, 21, 11)
        # Test Bounds
        self.assertTrue(field.is_centered(200, 100))
        self.assertAlmostEqual(100, field.get_height())
        self.assertAlmostEqual(2.0, field.get_aspect_ratio())
        # Test Prallelism & monotonicity
        self.assertFalse(field.horizontals_parallel)
        self.assertFalse(field.verticals_parallel)
        self.assertTrue(field.horizontal_monotone)
        self.assertTrue(field.vertical_monotone)

    def test_parallels(self):
        ratios =[]
        for standard_parallel in [0.0, np.arccos(2/np.pi), 1.0, -np.pi/3, np.pi/2.0]:
            transformation = get_winkel_tripel_projection(200,100, standard_parallel)
            field = TransformationField(transformation, 20, 10)
            ratios.append(field.get_aspect_ratio())
        for i in range(len(ratios)-1):
            self.assertGreater(ratios[i], ratios[i+1])
    

if __name__ == "__main__":
    unittest.main()