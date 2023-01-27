from cartography.projection_types import Pole
from map_extension import MapEffect
from cartography.projection import Projection

from cartography.projection_builder import ProjectionBuilder

class ApplyLambertAzimuthalEqualAreaEffect(MapEffect):

    def add_arguments(self, pars):
        super().add_arguments(pars)
        pars.add_argument("--pole", type=str, help="The projected pole")


    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        pole = Pole[self.options.pole]
        return projection_builder\
                        .to_lambert_azimuthal_equal_area(width, height, pole)\
                        .build()

if __name__ == '__main__':
    ApplyLambertAzimuthalEqualAreaEffect().run()
