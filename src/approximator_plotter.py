import enum
from cartography.approximator import equidistant_approximation
import matplotlib.pyplot as plt

def jump_function(t):
    sq_t = (t+4)*(t+4)
    if t < 0.5:
        return (t, sq_t)
    if t < 0.75:
        return (t , sq_t + 4)
    return (t , sq_t + 20)


def jump_parabola(t: float):
    scaled_t = 10*t
    if t < 0.5:
        return (scaled_t, scaled_t*scaled_t)
    return (scaled_t, scaled_t*scaled_t+10)
        

if __name__ == "__main__":
    points = equidistant_approximation(jump_function, 0.0, 1.0, 0.1, z_limit=1.0, z_fill=10)
    points = equidistant_approximation(jump_parabola, 0.0, 1.0, 0.001, 1, 40, 3.0, 5)
    x_values = [x for x,y in points]
    y_values = [y for x,y in points]
    for i, point in enumerate(points):
        print(i, point)
    plt.plot(x_values, y_values, marker="o")
    plt.show()

    