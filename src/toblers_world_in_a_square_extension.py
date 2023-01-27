from map_extension import MapEffect
from cartography.projection import Projection

from cartography.projection_builder import ProjectionBuilder

class ApplyToblersWorldInASquareEffect(MapEffect):
    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        return projection_builder\
                        .to_toblers_word_in_a_square(width, height, 0.0)\
                        .build()

if __name__ == '__main__':
    ApplyToblersWorldInASquareEffect().run()
