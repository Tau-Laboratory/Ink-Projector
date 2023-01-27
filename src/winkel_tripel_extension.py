from map_extension import MapEffect
from cartography.projection import Projection
import numpy as np
from cartography.projection_builder import ProjectionBuilder

class ApplyWinkelTripelEffect(MapEffect):
    def add_arguments(self, pars):
        super().add_arguments(pars)
        pars.add_argument("--standard_parallel", type=float, help="The Standard Parallel")

    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        standard_parallel = np.deg2rad(self.options.standard_parallel)
        return projection_builder\
                        .to_winkel_tripel(width, height, standard_parallel)\
                        .build()

if __name__ == '__main__':
    ApplyWinkelTripelEffect().run()
