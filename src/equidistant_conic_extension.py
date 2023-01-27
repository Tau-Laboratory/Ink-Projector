from map_extension import MapEffect
from cartography.projection import Projection

from cartography.projection_builder import ProjectionBuilder
from numpy import deg2rad

class ApplyEquidistantConicEffect(MapEffect):
    def add_arguments(self, pars):
        super().add_arguments(pars)
        pars.add_argument("--standard_latitude_a", type=float, help="The first standard parallel")
        pars.add_argument("--standard_latitude_b", type=float, help="The second standard parallel")

    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        standard_latitude_a = deg2rad(self.options.standard_latitude_a)
        standard_latitude_b = deg2rad(self.options.standard_latitude_b)
        return projection_builder\
                        .to_equidistant_conic(width, height, 0.0, 0.0, standard_latitude_a, standard_latitude_b)\
                        .build()

if __name__ == '__main__':
    ApplyEquidistantConicEffect().run()
