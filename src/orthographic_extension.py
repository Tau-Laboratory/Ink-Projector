from map_extension import MapEffect
from cartography.projection import Projection

from cartography.projection_builder import ProjectionBuilder
from numpy import deg2rad

class ApplyOrthographicEffect(MapEffect):
    def add_arguments(self, pars):
        super().add_arguments(pars)
        pars.add_argument("--origin_latitude", type=float, help="The latitude of the projection origin")
        pars.add_argument("--origin_longitude", type=float, help="The longitude of the projection origin")

    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        origin_latitude  = deg2rad(self.options.origin_latitude)
        origin_longitude = deg2rad(self.options.origin_longitude)

        return projection_builder\
                        .to_orthographic(width, height, (origin_longitude, origin_latitude))\
                        .build()

if __name__ == '__main__':
    ApplyOrthographicEffect().run()
