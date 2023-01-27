from map_extension import MapEffect
from cartography.projection import Projection

from cartography.projection_builder import ProjectionBuilder

class ApplyMollweideEffect(MapEffect):
    def add_arguments(self, pars):
        super().add_arguments(pars)
        pars.add_argument("--newton_raphson_precision", type=float, help="The projection iteration precision")

    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        newton_raphson_precision = self.options.newton_raphson_precision
        return projection_builder\
                        .to_mollweide(width, height, 0.0, newton_raphson_precision)\
                        .build()

if __name__ == '__main__':
    ApplyMollweideEffect().run()
