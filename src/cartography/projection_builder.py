from typing import Callable
from cartography.approximator import get_equidistant_approximator, get_linear_approximator
from cartography.projection import Projection
from cartography.transformations.map_transformation import *
from cartography.transformations.inverse_map_transformation import *
from cartography.projection_types import Point, Pole, Transformation, Bound, Approximator
from numpy import pi


class ProjectionBuilder:
    """
    The ProjectionBuilder is a simple builder pattern to create a Projection instance.
    """

    def __init__(self) -> None:
        self.inverse_transformation = None # type:Transformation
        self.visibility_bounds = ((-pi, -pi/2), (pi, pi/2)) # type:Bound
        self.transform = None # type:Transformation
        self.approximator = None # type:Approximator
        self.logger = None # type:Callable[[str], None]

    def from_equirectangular(self, width: float, height: float) -> "ProjectionBuilder":
        self.inverse_transformation = get_inverse_equirectangular_projection(width, height)
        return self

    def to_mercator(self, width: float, height: float, standard_longitude: float, latitude_limit: float) -> "ProjectionBuilder":
        self.transform = get_mercator_projection(width, height, standard_longitude, latitude_limit)
        return self

    def to_winkel_tripel(self, width: float, height: float, standard_latitude: float)-> "ProjectionBuilder":
        self.transform = get_winkel_tripel_projection(width, height, standard_latitude)
        return self
    
    def to_robinson(self, width: float, height: float, reference_longitude: float) -> "ProjectionBuilder":
        self.transform = get_robinson_projection(width, height, reference_longitude)
        return self
    
    def to_mollweide(self, width: float, height: float, reference_longitude: float, precision: float) -> "ProjectionBuilder":
        self.transform = get_mollweide_projection(width, height, reference_longitude, precision)
        return self

    def to_cylindrical_equal_area(self, width: float, height: float, reference_longitude: float, standard_latitude: float) -> "ProjectionBuilder":
        self.transform = get_cylindrical_equal_area_projection(width, height, reference_longitude, standard_latitude)
        return self

    def to_lambert(self, width: float, height: float, reference_longitude: float) -> "ProjectionBuilder":
        return self.to_cylindrical_equal_area(width, height, reference_longitude, 0.0)

    def to_behrmann(self, width: float, height: float, reference_longitude: float) -> "ProjectionBuilder":
        return self.to_cylindrical_equal_area(width, height, reference_longitude, 0.523598776)

    def to_smyth_equal_surface(self, width: float, height: float, reference_longitude: float) -> "ProjectionBuilder":
        return self.to_cylindrical_equal_area(width, height, reference_longitude, np.arccos(np.sqrt(2/np.pi)))

    def to_trystan_edwards(self, width: float, height: float, reference_longitude: float) -> "ProjectionBuilder":
        return self.to_cylindrical_equal_area(width, height, reference_longitude, 0.6527531402)

    def to_hobo_dyer(self, width: float, height: float, reference_longitude: float) -> "ProjectionBuilder":
        return self.to_cylindrical_equal_area(width, height, reference_longitude, 0.6544984695)

    def to_gall_peters(self, width: float, height: float, reference_longitude: float) -> "ProjectionBuilder":
        return self.to_cylindrical_equal_area(width, height, reference_longitude, 0.785398163)

    def to_balthasart(self, width: float, height: float, reference_longitude: float) -> "ProjectionBuilder":
        return self.to_cylindrical_equal_area(width, height, reference_longitude, 0.872664626)

    def to_toblers_word_in_a_square(self, width: float, height: float, reference_longitude: float) -> "ProjectionBuilder":
        return self.to_cylindrical_equal_area(width, height, reference_longitude, np.arccos(np.sqrt(1/np.pi)))


    def to_peirce_quincuncial(self, width: float, height: float, standard_longitude: float) -> "ProjectionBuilder":
        self.transform = get_peirce_quincuncial_projection(width, height, standard_longitude)
        return self

    def to_equidistant_conic(self, width: float, height: float, reference_longitude: float,\
        reference_latitiude: float, standard_latitude_a: float, standard_latitude_b: float) -> "ProjectionBuilder":
        self.transform = get_equidistant_conic_projection(width, height, reference_longitude, reference_latitiude, standard_latitude_a, standard_latitude_b)
        return self

    def to_orthographic(self, width: float, height: float, origin: Point) -> "ProjectionBuilder":
        self.transform = get_orthographic_projection(width, height, origin)
        return self

    def to_stereographic(self, width: float, height: float, latitude_limit: float, pole: Pole) -> "ProjectionBuilder":
        self.transform = get_stereographic_projection(width, height, latitude_limit, pole)
        return self

    def to_lambert_azimuthal_equal_area(self, width: float, height: float, pole: Pole) -> "ProjectionBuilder":
        self.transform = get_lambert_azimuthal_equal_area_projection(width, height, pole)
        return self

    def with_visibility_bounds(self, bounds: Bound) -> "ProjectionBuilder":
        self.visibility_bounds = bounds
        return self

    def with_linear_approximator(self, precision: float) -> "ProjectionBuilder":
        self.approximator = get_linear_approximator(precision)
        return self

    def with_equidistant_approximator(self, precision: float, maximal_resolution: int, increment: int, z_limit: float, z_fill: int) -> "ProjectionBuilder":
        self.approximator = get_equidistant_approximator(precision, maximal_resolution, increment, z_limit, z_fill)
        return self

    def with_logger(self, logger: Callable[[str], None]) -> "ProjectionBuilder":
        self.logger = logger
        return self

    def build(self) -> Projection:
        return Projection(self.inverse_transformation, self.visibility_bounds,\
            self.transform, self.approximator, self.logger)