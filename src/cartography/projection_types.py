from enum import Enum
from typing import Callable, Tuple, List

# Types used for typehinting

Point = Tuple[float, float]
Bound = Tuple[Point, Point]
Producer = Callable[[float], Point]
Transformation = Callable[[float, float], Point]
Approximator = Callable[[Producer], List[Point]]

class Pole(Enum):
    NORTHPOLE = 0
    SOUTHPOLE = 1