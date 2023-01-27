from map_extension import MapEffect
from cartography.projection import Projection

from cartography.projection_builder import ProjectionBuilder
from numpy import pi, deg2rad

class ApplyMercatorEffect(MapEffect):
    def add_arguments(self, pars):
        super().add_arguments(pars)
        pars.add_argument("--latitude_limit", type=float, help="The latitude cutoff")

    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        latitude_limit = deg2rad(self.options.latitude_limit)
        return projection_builder\
                        .to_mercator(width, height, 0.0, latitude_limit)\
                        .build()
        
if __name__ == '__main__':
    ApplyMercatorEffect().run()
