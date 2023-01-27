from tests.test_2D import Test2D
from cartography.transformations.inverse_map_transformation import get_inverse_equirectangular_projection
from numpy import linspace, pi

class InverseEquirectangularTest(Test2D):
    def test_transformation(self):
        width, height = 400, 200
        resolution = 100
        transform = get_inverse_equirectangular_projection(width, height)

        x_points = linspace(0.0, width, resolution)
        y_points = linspace(0.0, height, resolution)
        long_points = linspace(-pi, pi, resolution)
        lat_points = linspace(-pi/2, pi/2, resolution)

        for i in range(resolution):
            for j in range(resolution):
                point_in = (x_points[i], y_points[j])
                point_out = (long_points[i], lat_points[j])
                self.assertPointEqual(point_out, transform(*point_in))