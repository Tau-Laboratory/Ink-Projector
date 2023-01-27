from map_extension import MapEffect
from cartography.projection import Projection

from cartography.projection_builder import ProjectionBuilder

class ApplyPeirceQuincuncialEffect(MapEffect):
    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        return projection_builder\
                        .to_peirce_quincuncial(width, height, 0.0)\
                        .build()

if __name__ == '__main__':
    ApplyPeirceQuincuncialEffect().run()
