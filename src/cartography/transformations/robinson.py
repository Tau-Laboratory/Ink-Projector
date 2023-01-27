import numpy as np
from cartography.projection_types import Point
from cartography.cubic_spline import CubicSplineInterpolator

_robinson_table = {
    0 : (1.0000, 0.0000),
    5 : (0.9986, 0.0620),
    10: (0.9954, 0.1240),
    15: (0.9900, 0.1860),
    20: (0.9822, 0.2480),
    25: (0.9730, 0.3100),
    30: (0.9600, 0.3720),
    35: (0.9427, 0.4340),
    40: (0.9216, 0.4958),
    45: (0.8962, 0.5571),
    50: (0.8679, 0.6176),
    55: (0.8350, 0.6769),
    60: (0.7986, 0.7346),
    65: (0.7597, 0.7903),
    70: (0.7186, 0.8435),
    75: (0.6732, 0.8936),
    80: (0.6213, 0.9394),
    85: (0.5722, 0.9761),
    90: (0.5322, 1.0000)
}

_robinson_latitudes = [5*i for i in range(19)]
_robinson_x_values = [_robinson_table[i][0] for i in _robinson_latitudes]
_robinson_y_values = [_robinson_table[i][1] for i in _robinson_latitudes]

_robinson_x_spline = CubicSplineInterpolator(_robinson_latitudes, _robinson_x_values)
_robinson_y_spline = CubicSplineInterpolator(_robinson_latitudes, _robinson_y_values)

def get_robinson_factors(latitiude: float) -> Point:
    """
    Implementation of the Robinson lookup table. 
    It uses cubic spline interpolation for any points between the set values.
    """
    factor_sign = np.sign(latitiude)
    absolute_latitiude_in_degrees = abs(latitiude)* 180 / np.pi
    x = _robinson_x_spline.evaluate(absolute_latitiude_in_degrees)
    y = _robinson_y_spline.evaluate(absolute_latitiude_in_degrees)
    return x, y*factor_sign