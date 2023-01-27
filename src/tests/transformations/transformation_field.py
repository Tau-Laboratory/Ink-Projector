from typing import List
from cartography.projection_types import Point, Transformation, Bound
import numpy as np

class TransformationField():
    def __init__(self, transformation: Transformation, x_resolution = 200, y_resolution = 100) -> None:
        x_linspace = np.linspace(-np.pi, np.pi, x_resolution)
        y_linspace = np.linspace(-np.pi/2, np.pi/2, y_resolution)
        
        self.points = [[transformation(x,y) for y in y_linspace] for x in x_linspace]
        self._compute_point_stats()
        self.bounds = self._get_bounds()
    
    def _get_bounds(self) -> Bound:
        x_min, y_min = x_max, y_max = self.points[0][0]
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                x,y = self.points[i][j]
                x_min = min(x_min, x)
                x_max = max(x_max, x)
                y_min = min(y_min, y)
                y_max = max(y_max, y)
        return ((x_min, y_min), (x_max, y_max))
    
    def get_width(self) -> float:
        return self.bounds[1][0] - self.bounds[0][0]
    
    def get_height(self) -> float:
        return self.bounds[1][1] - self.bounds[0][1]
    
    def get_aspect_ratio(self) -> float:
        return self.get_width() / self.get_height()

    def is_centered(self, width: float, height: float, delta = 0.00001) -> bool:
        x_diff = abs(self.bounds[0][0] - (width - self.bounds[1][0])) 
        y_diff = abs(self.bounds[0][1] - (height - self.bounds[1][1])) 
        x_centered = x_diff <= delta
        y_centered = y_diff <= delta
        return x_centered and y_centered

    def _compute_point_stats(self):
        delta = 0.0001
        # Parallel
        self.horizontals_parallel = True
        self.verticals_parallel = True
        # Monotonicity
        self.horizontal_monotone = True
        self.vertical_monotone = True

        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                x,y = self.points[i][j]
                if i > 0:
                    x_prev, y_prev = self.points[i-1][j]
                    self.verticals_parallel = self.verticals_parallel and abs(y-y_prev) <= delta

                    self.horizontal_monotone = self.horizontal_monotone and x >= x_prev
                if j > 0:
                    x_prev, y_prev = self.points[i][j-1]
                    self.horizontals_parallel = self.horizontals_parallel and abs(x-x_prev)<=delta

                    self.vertical_monotone = self.vertical_monotone and y >= y_prev
                    
    def has_horizontal_circles(self, center: Point) -> bool:
        delta = 0.0001
        center_x, center_y = center
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                x,y = self.points[i][j]
                radius_squared = (x-center_x)**2 + (y-center_y)**2
                if i > 0:
                     x_prev, y_prev = self.points[i-1][j]
                     prev_radius_squared = (x_prev - center_x) ** 2 + (y_prev - center_y)**2
                     if abs(radius_squared - prev_radius_squared) > delta:
                        return False
        return True

    def get_horizontal_circle_radii(self, center: Point) -> List[float]:
        center_x, center_y = center
        radii = []
        for i in range(len(self.points[0])):
            x,y = self.points[0][i]
            radii.append( ((x-center_x)**2 + (y-center_y)**2)**(1/2) )
        return radii