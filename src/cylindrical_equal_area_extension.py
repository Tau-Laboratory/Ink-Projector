from map_extension import MapEffect
from cartography.projection import Projection

from cartography.projection_builder import ProjectionBuilder
from numpy import deg2rad

class ApplyCylindricalEqualAreaEffect(MapEffect):
    def add_arguments(self, pars):
        super().add_arguments(pars)
        pars.add_argument("--standard_latitude", type=float, help="The standard parallels")

    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        standard_latitude = deg2rad(self.options.standard_latitude)
        return projection_builder\
                        .to_cylindrical_equal_area(width, height, 0.0, standard_latitude)\
                        .build()

if __name__ == '__main__':
    ApplyCylindricalEqualAreaEffect().run()
