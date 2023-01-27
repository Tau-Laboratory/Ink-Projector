from math import inf
from cartography.projection_types import Bound, Transformation
import numpy as np

from cartography.transformations.map_transformation import get_cylindrical_equal_area_projection, get_mercator_projection, get_mollweide_projection, get_peirce_quincuncial_projection, get_robinson_projection, get_winkel_tripel_projection

def get_bounds(transformation: Transformation, input_bound: Bound, sample_count: int) -> Bound:
    lower, upper = input_bound
    low_x, low_y = lower
    high_x, high_y = upper

    min_x = inf
    min_y = inf
    max_x = -inf
    max_y = -inf

    x_space = np.linspace(low_x, high_x, sample_count)
    y_space = np.linspace(low_y, high_y, sample_count)
    for x in x_space:
        for y in y_space:
            test_x, test_y = transformation(x,y)
            min_x = min(min_x, test_x)
            max_x = max(max_x, test_x)
            min_y = min(min_y, test_y)
            max_y = max(max_y, test_y)
    return ((min_x, min_y), (max_x, max_y))

def get_lat_long_bound(transformation: Transformation, sample_count: int) -> Bound:
    return get_bounds(transformation, ((-np.pi,-np.pi/2.0),(np.pi, np.pi/2.0)), sample_count)

def format_bounds(bound: Bound) -> str:
    lower, upper = bound
    low_x, low_y = lower
    high_x, high_y = upper

    return f"X: [{low_x}, {high_x}], Y: [{low_y}, {high_y}]"

if __name__ == "__main__":
    hobo_dyer = get_cylindrical_equal_area_projection(500, 250, 0.0, 0.6544984695)
    hobo_dyer_bounds = get_lat_long_bound(hobo_dyer, 15)
    print("Hobo:", format_bounds(hobo_dyer_bounds))