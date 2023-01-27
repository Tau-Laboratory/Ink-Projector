from cartography.projection_types import Bound, Transformation, Point
from numpy import pi


def get_linear_transform(old_bounds: Bound, new_bounds: Bound) -> Transformation:
    """
    Returns a function that transforms any point from the space defined by the old bounds into a point from the space defined by the new bounds
    bounds are pairs of points with the first point being the lower and the second point being the heigher bound
    """
    old_min, old_max = old_bounds
    old_min_x, old_min_y = old_min
    old_max_x, old_max_y = old_max

    new_min, new_max = new_bounds
    new_min_x, new_min_y = new_min
    new_max_x, new_max_y = new_max

    def transform(x: float, y: float) -> Point:
        x_normalized = (x-old_min_x) / (old_max_x - old_min_x) 
        new_x = x_normalized * (new_max_x - new_min_x) + new_min_x

        y_normalized = (y-old_min_y) / (old_max_y - old_min_y) 
        new_y = y_normalized * (new_max_y - new_min_y) + new_min_y
        return (new_x, new_y)
    
    return transform

def get_circle_bound(x_radius=1.0, y_radius=1.0) -> Bound:
    """
    Returns the bound required to fit a circle or axis-aligned ellipse with the provided radii perfectly inside it.
    """
    return ((-x_radius, -y_radius), (x_radius, y_radius))

def get_centered_square_bound(width: float, height: float) -> Bound:
    """
    Returns the bound of the biggest possible square that fits within the provided rectangle. 
    The Square will be centered to the rectangles dimensions.
    """
    width_min  = max(0.0, width - height) * 0.5
    height_min = max(0.0, height - width) * 0.5
    width_max  = min(width, height) + width_min
    height_max = min(width, height) + height_min
    return ((width_min, height_min), (width_max, height_max))

def get_rectangle_bound(width: float, height: float)-> Bound:
    """
    Returns the bound for a rectangle with the given width and height starting at (0,0)
    """
    return ((0,0),(width, height))

def get_long_lat_bound() -> Bound:
    """
    Returns the Bound of the longitude-latitude space
    """
    return ((-pi, -pi/2),(pi, pi/2))

def get_transform_to_fit(old_bounds: Bound, width: float, height: float) -> Transformation:
    """ 
    Returns a function that scales anything from the old bound to a bound that fits perfectly 
    into the given width and height whilst maintaining the same aspect ratio.
    """
    old_lower, old_higher = old_bounds
    x_min, y_min = old_lower
    x_max, y_max = old_higher
    
    old_width  = x_max - x_min
    old_height = y_max - y_min
    aspect_ratio = old_width / old_height

    if aspect_ratio*height <= width:
        scaled_width = height * aspect_ratio
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = scaled_width / aspect_ratio
    
    x_offset = (width - scaled_width) / 2
    y_offset = (height - scaled_height) / 2

    new_bounds = ((x_offset, y_offset),(x_offset+scaled_width, y_offset+scaled_height))
    return get_linear_transform(old_bounds, new_bounds)
