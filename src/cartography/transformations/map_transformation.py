from cartography.transformations.generic_transformation import get_centered_square_bound, get_linear_transform, get_long_lat_bound, get_rectangle_bound, get_circle_bound, get_transform_to_fit
import numpy as np
from numpy import sin, cos, sinc, arccos, tan, pi, sqrt
from cartography.basis_function import get_clamp
from cartography.transformations.peirce_quincuncial import PeirceQuincuncialScale, toPeirceQuincuncial

from cartography.projection_types import *
from cartography.transformations.robinson import get_robinson_factors

"""
Latitude: North-South Angle (+90 = pi/2 = Northpole, -90 = -pi/2 = Southpole) 
Longitude: East- West Angle (+140 = Tokyo, -122 = San Francisco) +180 = pi => -180 = -pi
"""


# Full Map Transformations
def get_mercator_projection(width: float, height: float, standard_longitude: float, latitude_limit: float) -> Transformation:
    # https://en.wikipedia.org/wiki/Mercator_projection
    
    clamp = get_clamp(((-np.pi-standard_longitude, -latitude_limit),(np.pi-standard_longitude, latitude_limit)))
    extreme = np.log(np.tan(pi/4 + latitude_limit/2))
    old_bound = ((-np.pi-standard_longitude, -extreme),(np.pi-standard_longitude, extreme))
    scaler = get_transform_to_fit(old_bound, width, height)

    def transform(longitude: float, latitude: float) -> Point:
        #Step 1 Clamp the latitude
        longitude, latitude = clamp(longitude-standard_longitude, latitude)
        # Step 2 Compute the latitude
        latitude = np.log(np.tan(np.pi/4 + latitude/2))
        # Step 3 Scale to the map size
        return scaler(longitude, latitude)   
    return transform

def get_winkel_tripel_projection(width: float, height: float, standard_latitude: float) -> Transformation:
    # https://en.wikipedia.org/wiki/Winkel_tripel_projection
    def transform_unscaled(longitude: float, latitiude: float) -> Point:
        # We divide by pi since numpy's sinc function is normalized
        alpha = arccos(cos(latitiude)*cos(longitude/2)) / pi
        x = 0.5 * ( (longitude * cos(standard_latitude)) + ((2*cos(latitiude)*sin(longitude/2))/sinc(alpha))) 
        y = 0.5 * ( latitiude + sin(latitiude)/sinc(alpha))
        return x,y

    x_min,_ = transform_unscaled(-np.pi, 0.0)
    x_max,_ = transform_unscaled(np.pi, 0.0)
    _,y_min = transform_unscaled(0.0, -np.pi/2)
    _,y_max = transform_unscaled(0.0, np.pi/2)

    old_bound = ((x_min,y_min),(x_max, y_max))
    scaler = get_transform_to_fit(old_bound, width, height)
    def transform(longitude: float, latitiude: float) -> Point:
        # We divide by pi since numpy's sinc function is normalized
        alpha = arccos(cos(latitiude)*cos(longitude/2)) / pi
        x = 0.5 * ( (longitude * cos(standard_latitude)) + ((2*cos(latitiude)*sin(longitude/2))/sinc(alpha))) 
        y = 0.5 * ( latitiude + sin(latitiude)/sinc(alpha))
        return scaler(x, y) 
    return transform

def get_robinson_projection(width: float, height: float, reference_longitude: float) -> Transformation:
    # https://en.wikipedia.org/wiki/Robinson_projection
    x_bound = 0.8487 * pi
    y_bound = 1.3523
    old_bound = ((-x_bound, -y_bound),(x_bound, y_bound))
    scaler = get_transform_to_fit(old_bound, width, height)   

    def transform(longitude: float, latitude: float)-> Point:
        X_factor, Y_factor = get_robinson_factors(latitude)
        x = 0.8487 * X_factor * (longitude - reference_longitude)
        y = 1.3523 * Y_factor
        return scaler(x,y)
    return transform

def get_mollweide_projection(width: float, height: float, reference_longitude: float, precision: float) -> Transformation:
    # https://en.wikipedia.org/wiki/Mollweide_projection
    def newton_raphson_iteration(theta: float, latitude: float) -> float:
        cos_theta = cos(theta)
        if cos_theta == 0:
            return latitude
        numerator = 2*theta + sin(2*theta) - pi*sin(latitude)
        divisor = 4 * (cos_theta**2)
        return theta - (numerator / divisor)

    old_bound = get_circle_bound()
    scaler = get_transform_to_fit(old_bound, width, height)

    def transform(longitude: float, latitude: float)-> Point:
        perv_theta = latitude
        theta = newton_raphson_iteration(perv_theta, latitude)
        while(abs(theta-perv_theta) > precision):
            perv_theta, theta = theta, newton_raphson_iteration(theta, latitude)

        x = (longitude - reference_longitude) * cos(theta)*2 / pi
        y = sin(theta)
        return scaler(x,y)
    return transform

def get_cylindrical_equal_area_projection(width: float, height: float, reference_longitude: float, standard_latitude: float) -> Transformation:
    # https://en.wikipedia.org/wiki/Cylindrical_equal-area_projection
    aspect_ratio = cos(standard_latitude)**2 * pi
    x_min = (-pi - reference_longitude)
    x_max = (pi - reference_longitude)
    y_min = -1
    y_max =  1
    old_bounds = ((x_min, y_min),(x_max, y_max))

    if aspect_ratio*height <= width:
        scaled_width = height * aspect_ratio
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = scaled_width / aspect_ratio
    
    x_offset = (width - scaled_width) / 2
    y_offset = (height - scaled_height) / 2

    new_bounds = ((x_offset, y_offset),(x_offset+scaled_width, y_offset+scaled_height))
    scaler = get_linear_transform(old_bounds, new_bounds)
    
    def transform(longitude: float, latitude: float)-> Point:
        x = (longitude - reference_longitude)
        y = sin(latitude)
        return scaler(x,y)
    return transform

def get_peirce_quincuncial_projection(width: float, height: float, standard_longitude: float) -> Transformation:
    # https://en.wikipedia.org/wiki/Peirce_quincuncial_projection
    old_bound = get_circle_bound(PeirceQuincuncialScale, PeirceQuincuncialScale)
    new_bound = get_centered_square_bound(width, height)
    scaler = get_linear_transform(old_bound, new_bound)

    def transform(longitude: float, latitude: float)-> Point:
        x,y =  toPeirceQuincuncial(longitude, latitude, standard_longitude)
        return scaler(x,y)
    return transform

# Middeling Projections

def get_equidistant_conic_projection(width: float, height: float, reference_longitude: float,\
    reference_latitiude: float, standard_latitude_a: float, standard_latitude_b: float) -> Transformation:
    # https://en.wikipedia.org/wiki/Equidistant_conic_projection
    if standard_latitude_a == standard_latitude_b:
        n = sin(standard_latitude_a)
    else:
        n = (cos(standard_latitude_a) - cos(standard_latitude_b)) / (standard_latitude_b - standard_latitude_a)
    
    if n == 0.0:
        # We have either 
        #   standard_latitude_a = standard_latitude_b = 0.0 
        # OR
        #   standard_latitude_a = -standard_latitude_b
        # In this case we return the equirectangular projection as the conic projection converges to it at these points
        old_bound = get_long_lat_bound()
        new_bound = get_rectangle_bound(width, height)
        return get_linear_transform(old_bound, new_bound)

    G = cos(standard_latitude_a) / n + standard_latitude_a
    rho_0 = G - reference_latitiude
    def unscaled_conical_projection(longitude: float, latitude: float) -> Point:
        rho = G - latitude
        x = rho *  sin(n*(longitude - reference_longitude))
        y = rho_0 - rho * cos(n*(longitude- reference_longitude))
        return x,y

    # We compute the boundaries for scaling by just checking the extreme values
    # Extreme Points of Conical Projection
    # corners: long = +/- pi, lat = +/- pi/2
    # center edges = long = 0, lat = +/- pi2
    corner_a = unscaled_conical_projection(-np.pi, -pi/2)
    corner_b = unscaled_conical_projection(-np.pi, +pi/2)
    corner_c = unscaled_conical_projection(+np.pi, -pi/2)
    corner_d = unscaled_conical_projection(+np.pi, +pi/2)
    edge_a   =  unscaled_conical_projection(0, -pi/2)
    edge_b   =  unscaled_conical_projection(0, +pi/2)

    xMin = min(corner_a[0], corner_b[0], corner_c[0], corner_d[0])
    xMax = max(corner_a[0], corner_b[0], corner_c[0], corner_d[0])
    yMin = min(corner_a[1], corner_b[1], corner_c[1], corner_d[1], edge_a[1], edge_b[1])
    yMax = max(corner_a[1], corner_b[1], corner_c[1], corner_d[1], edge_a[1], edge_b[1])

    old_bound = ((xMin, yMin),(xMax, yMax))
    scaler = get_transform_to_fit(old_bound, width, height)
    def transform(longitude: float, latitude: float) -> Point:
        x,y = unscaled_conical_projection(longitude, latitude)
        return scaler(x,y)
    return transform

# Polar Projections

def get_orthographic_projection(width: float, height: float, origin: Point) -> Transformation:
    # https://en.wikipedia.org/wiki/Orthographic_map_projection

    origin_long, origin_lat = origin
    old_bound = get_circle_bound()
    new_bound = get_centered_square_bound(width, height)
    scaler = get_linear_transform(old_bound, new_bound)

    def transform(longitude: float, latitude: float) -> Point:
        x = cos(latitude) * sin(longitude - origin_long)
        y = (cos(origin_lat)*sin(latitude)) - (sin(origin_lat) * cos(latitude) * cos(longitude - origin_long))

        angular_distance = (sin(origin_lat)* sin(latitude)) + (cos(origin_lat) * cos(latitude) * cos(longitude - origin_long))
        if angular_distance < 0.0:
            # The Point is at the oposite side of the planet
            # We'll camp it to the perimeter
            if x != 0.0 or y != 0.0:
                # Normalize x,y
                norm = np.linalg.norm((x,y))
                x = x / norm
                y = y / norm
            else:
                # Default for the opposite pole
                x = 0.0
                y = 1.0
        return scaler(x, y)
    return transform

def get_stereographic_projection(width: float, height: float, latitude_limit: float, pole: Pole) -> Transformation:
    # https://en.wikipedia.org/wiki/Stereographic_map_projection
    projection_radius = min(width, height) * 0.5
    x_center = max(0.0, width - height) * 0.5 + projection_radius
    y_center = max(0.0, height - width) * 0.5 + projection_radius

    if pole is Pole.NORTHPOLE:
        clamp = get_clamp(((-np.pi, -np.pi/2),(np.pi, latitude_limit)))
        normalization_factor = tan(pi/4 + latitude_limit / 2.0)
    else:
        clamp = get_clamp(((-np.pi, latitude_limit),(np.pi, np.pi/2)))
        normalization_factor = tan(pi/4 - latitude_limit / 2.0)
    
    def transform(longitude: float, latitiude: float)-> Point:
        longitude, latitiude = clamp(longitude, latitiude)
        angle = 0.0
        if pole is Pole.NORTHPOLE:
            angle = pi/4 + latitiude/2.0
        if pole is Pole.SOUTHPOLE:
            angle = pi/4 - latitiude/2.0
        radius = projection_radius * tan(angle) / normalization_factor
        x = x_center + radius * cos(longitude)
        y = y_center + radius * sin(longitude)
        return x,y
    return transform

def get_lambert_azimuthal_equal_area_projection(width: float, height: float, pole: Pole) -> Transformation:
    # https://en.wikipedia.org/wiki/Lambert_azimuthal_equal-area_projection
    projection_radius = min(width, height) * 0.5
    x_center = max(0.0, width - height) * 0.5 + projection_radius
    y_center = max(0.0, height - width) * 0.5 + projection_radius

    def transform(longitude: float, latitiude: float)-> Point:
        if pole is Pole.NORTHPOLE:
            colatitude = pi/2 + latitiude
        else:
            colatitude = pi/2 - latitiude
        radius = projection_radius * sin(colatitude/2)
        x = x_center + radius * cos(longitude)
        y = y_center + radius * sin(longitude)
        return x,y
    return transform
