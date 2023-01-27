from cartography.projection_types import Bound, Point, Producer, Transformation
import numpy as np
from numpy import sin, cos, abs as np_abs, deg2rad, sqrt, pi

def get_line_function(line_start: Point, line_end: Point)-> Producer:
    """
    Returns a linear function with f(0)=start and f(1)=end
    """
    from_x, from_y = line_start
    to_x, to_y = line_end

    delta_x = to_x - from_x
    delta_y = to_y - from_y

    def line(t: float) -> Point:
        x = from_x + t * delta_x
        y = from_y + t * delta_y
        return x,y
    
    return line

def get_quadratic_bezier_function(curve_start: Point, control_point_a: Point, curve_end: Point) -> Producer:
    """
    Returns a quadratic Bezier with f(0)=start and f(1)=end
    using the provided control point
    """
    from_x, from_y = curve_start
    a_x, a_y = control_point_a
    to_x, to_y = curve_end

    def curve(t: float) -> Point:
        t_bar = 1-t

        x = from_x * (t_bar ** 2)
        y = from_y * (t_bar ** 2)

        x += a_x * t_bar * t * 2
        y += a_y * t_bar * t * 2

        x += to_x * (t ** 2)
        y += to_y * (t ** 2)
        return x, y

    return curve

def get_cubic_bezier_function(curve_start: Point, control_point_a: Point, control_point_b: Point, curve_end: Point) -> Producer:
    """
    Returns a cubic Bezier with f(0)=start and f(1)=end
    using the provided control points
    """
    from_x, from_y = curve_start
    a_x, a_y = control_point_a
    b_x, b_y = control_point_b
    to_x, to_y = curve_end

    def curve(t: float) -> Point:
        t_bar = 1-t

        x = from_x * (t_bar ** 3)
        y = from_y * (t_bar ** 3)

        x += a_x * (t_bar ** 2) * t * 3
        y += a_y * (t_bar ** 2) * t * 3

        x += b_x * t_bar * (t ** 2) * 3
        y += b_y * t_bar * (t ** 2) * 3

        x += to_x * (t ** 3)
        y += to_y * (t ** 3)
        return x, y

    return curve

def get_arc_function(curve_start: Point, curve_end: Point, radii: Point, x_angle_in_degrees: float, large_arc: bool, sweep_arc: bool) -> Producer:
    """
    Returns an arc with f(0)=start and f(1)=end
    using the provided radii and svg parameters
    """
    # Based on https://mortoray.com/rendering-an-svg-elliptical-arc-as-bezier-curves/
    radius_x, radius_y = np_abs(radii)
    x_angle = deg2rad(x_angle_in_degrees)

    dx_over_two = (curve_start[0] - curve_end[0]) / 2.0
    dy_over_two = (curve_start[1] - curve_end[1]) / 2.0
    
    x1p = cos(x_angle) * dx_over_two + sin(x_angle) * dy_over_two
    y1p = -sin(x_angle) * dx_over_two + cos(x_angle) * dy_over_two

    radius_x_squared = radius_x ** 2
    radius_y_squared = radius_y ** 2

    x1p_squared = x1p ** 2 
    y1p_squared = y1p ** 2

    # check if the radius is too small `pq < 0`, when `dq > radius_x_squared * radius_y_squared` (see below)
    # circle_ratio is the ratio (dq : rxs * rys) 
    circle_ratio = x1p_squared/radius_x_squared + y1p_squared/radius_y_squared
    if (circle_ratio > 1):
        # scale up rX,rY equally so circle_ratio == 1
        scaler = sqrt(circle_ratio)
        radius_x *= scaler
        radius_y *= scaler
        radius_x_squared = radius_x ** 2
        radius_y_squared = radius_y ** 2
    
    dq = (radius_x_squared * y1p_squared + radius_y_squared * x1p_squared)
    pq = (radius_x_squared * radius_y_squared - dq) / dq
    q = sqrt(max(0,pq)) # use Max to account for float precision
    if (large_arc == sweep_arc):
        q = -q
    cxp = q * radius_x * y1p / radius_y
    cyp = - q * radius_y * x1p / radius_x

    center_x = cos(x_angle)*cxp - sin(x_angle)*cyp + (curve_start[0] + curve_end[0]) / 2.0;
    center_y = sin(x_angle)*cxp + cos(x_angle)*cyp + (curve_start[1] + curve_end[1]) / 2.0;

    theta = _svg_angle( 1, 0, (x1p-cxp) / radius_x, (y1p - cyp)/ radius_y )
    delta = _svg_angle(
        (x1p - cxp)/radius_x, (y1p - cyp)/radius_y,
        (-x1p - cxp)/radius_x, (-y1p-cyp)/radius_y)
    delta %= pi * 2
    if not sweep_arc:
        delta -= 2 * pi

    start_angle = theta
    angle_size = delta

    def arc(t: float) -> Point:
        arc_angle = start_angle + t * angle_size
        x = center_x + radius_x * cos(x_angle) * cos(arc_angle) - radius_y * sin(x_angle) * sin(arc_angle)
        y = center_y + radius_x * sin(x_angle) * cos(arc_angle) + radius_y * cos(x_angle) * sin(arc_angle)
        return x, y 
    
    return arc

def _svg_angle(ux: float, uy: float, vx: float, vy:float) -> float:
    u = np.array([ux, uy])
    v = np.array([vx, vy])

    dot = np.dot(u,v)
    v_len = np.linalg.norm(u) * np.linalg.norm(v)
    ang = np.arccos( min(max(dot / v_len,-1),1))  # floating point precision, slightly over values appear
    if ( (ux *vy - uy*vx) < 0):
        ang = -ang
    return ang

def get_clamp(clamp_bound: Bound) -> Transformation:
    """
    Returns a function that clamps any coordinate into the given bound.
    """
    min_bound, max_bound = clamp_bound
    x_min, y_min = min_bound
    x_max, y_max = max_bound

    def clamp(x: float, y: float)-> Point:
        x_clamped = min(x_max, max(x_min, x))
        y_clamped = min(y_max, max(y_min, y))
        return x_clamped, y_clamped
    return clamp