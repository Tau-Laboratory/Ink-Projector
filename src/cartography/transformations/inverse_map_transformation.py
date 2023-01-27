from numpy import pi
from cartography.transformations.generic_transformation import get_linear_transform
from cartography.projection_types import Transformation

def get_inverse_equirectangular_projection(width: float, height: float) -> Transformation:
    """
    Transforms an equirectangular map back into the longitude, latitude space.
    """
    xy_bounds = ((0,0),(width, height))
    longitude_latitude_bounds = ((-pi,-pi/2.0),(pi, pi/2.0))
    return get_linear_transform(xy_bounds, longitude_latitude_bounds)