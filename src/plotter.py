import matplotlib.pyplot as plt
from cartography.basis_function import *
import numpy as np

"""
cubic = get_cubic_bezier_function((0,0), (0, 2), (2,2), (2, 0))
t_values = np.linspace(0, 1, 100)
x_values, y_values = cubic(t_values)

plt.plot([0, 0, 2, 2], [0, 2, 2, 0], marker="o")
plt.plot(x_values, y_values)
plt.show()
"""

#arc = get_arc_function((110, -215), (162.55, -162.45), (30,50), 0.0, True, False)

t_values = np.linspace(0, 1, 100)
"""
arc = get_arc_function((0,0), (5,5), (5,5), 0, False, False )
x_values, y_values = arc(t_values)
plt.plot(x_values, y_values)

"""
arc = get_arc_function((0,0), (5,5), (5,5), 0, True, False )
x_values, y_values = arc(t_values)
plt.plot(x_values, y_values)
"""
arc = get_arc_function((0,0), (5,5), (5,5), 0, False, True )
x_values, y_values = arc(t_values)
plt.plot(x_values, y_values)
"""
arc = get_arc_function((0,0), (5,5), (5,5), 0, True, True )
x_values, y_values = arc(t_values)
plt.plot(x_values, y_values)

plt.show()