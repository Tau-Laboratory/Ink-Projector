from map_extension import MapEffect
from cartography.projection import Projection

from cartography.projection_builder import ProjectionBuilder

class ApplyHoboDyerEffect(MapEffect):
    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        return projection_builder\
                        .to_hobo_dyer(width, height, 0.0)\
                        .build()

if __name__ == '__main__':
    ApplyHoboDyerEffect().run()
