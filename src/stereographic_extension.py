from cartography.projection_types import Pole
from map_extension import MapEffect
from cartography.projection import Projection

from cartography.projection_builder import ProjectionBuilder
from numpy import deg2rad

class ApplyStereographicEffect(MapEffect):
    def add_arguments(self, pars):
        super().add_arguments(pars)
        pars.add_argument("--latitude_limit", type=float, help="The latitude cutoff")
        pars.add_argument("--pole", type=str, help="The projected pole")

    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        latitude_limit = deg2rad(self.options.latitude_limit)
        pole = Pole[self.options.pole]
        return projection_builder\
                        .to_stereographic(width, height, latitude_limit , pole)\
                        .build()

if __name__ == '__main__':
    ApplyStereographicEffect().run()
