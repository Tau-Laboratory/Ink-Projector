from cartography.basis_function import *
from inkex.elements import PathElement
from inkex.transforms import BoundingBox, Transform
from inkex.paths import Path, Move, Line, Vert, Horz, Arc, Curve, Smooth, Quadratic, ZoneClose, TepidQuadratic
from cartography.projection_types import *


class Projection:
    """
    The Projection class takes in PathElements and transforms them to a different projection.
    They do this by first applying the inverse transformation of the current projection
    followed by the transformation to the desired projection.
    """
    def __init__(self,\
        inverse_transformation: Transformation,\
        visibility_bounds: Bound,\
        transform: Transformation,\
        approximator: Approximator,\
        logger: Callable[[str],None]) -> None:
        self.from_transform = inverse_transformation
        self.bounds = visibility_bounds
        self.bound_clamp = get_clamp(self.bounds)
        self.to_transform = transform
        self.approximator = approximator
        self.logger = logger
        if logger is None:
            self.logger = lambda x: None
            
        
    def transform(self, path_element: PathElement):
        """
        Transforms a given PathElement to the new projection.
        If the element is empty or it is outside the visible area it will be deleted.
        """
        transformation_to_relative_coordinates = self._convert_to_absolute_coordinates(path_element)

        path_empty = len(path_element.path) == 0
        if path_empty:
            # self.logger(f"Path \"{path_element.label}\" is empty and was discarded.")
            path_element.delete()
            return

        if not self._bounds_intersect_visibility(path_element.bounding_box()):
            # The Path is fully invisible and thus does not need to be transformed
            # self.logger(f"Path \"{path_element.label}\" is outside of the projection bounds and was discarded.")
            path_element.delete()
            return

        self._current_x_untransformed = 0.0
        self._current_y_untransformed = 0.0
        self._start_x_untransformed = None
        self._start_y_untransformed = None
        self.transformed_path = []

        path = path_element.path # type:Path
        path = path.to_non_shorthand() # type:Path
        for command in path:
            if isinstance(command, Move):
                self._transform_move(command)
            elif isinstance(command, Line):
                self._transform_line(command)
            elif isinstance(command, Vert):
                self._transform_line(Line(self._current_x_untransformed, command.y))
            elif isinstance(command, Horz):
                self._transform_line(Line(command.x, self._current_y_untransformed))
            elif isinstance(command, Arc):
                self._transform_arc(command)
            elif isinstance(command, Curve):
                self._transform_cubic(command)
            elif isinstance(command, Quadratic):
                self._transform_quadratic(command)
            elif isinstance(command, ZoneClose):
                # Insert a line to the start
                self._transform_line(Line(self._start_x_untransformed, self._start_y_untransformed))
                self.transformed_path.append(command)
                # We start a new zone and reset the start point
                self._start_x_untransformed = None
                self._start_y_untransformed = None
            else:
                # Default: identity
                self.logger(f"Unsupported Command {type(command)} in path {path_element.label}")
                # self.transformed_path.append(command)
        path_element.path = self.transformed_path
        self._convert_to_relative_coodinates(path_element, transformation_to_relative_coordinates)
    
    def _convert_to_absolute_coordinates(self, path_element: PathElement) -> Transform:
        """
        All projections should be done relative to absolute coordinates.
        As a result we have to apply any group transformations and undo them after the fact.
        This function applies all transformations and computes the inverse so the 
        transformation can be undone after the projection is done.
        """
        transformation_to_absolute_coordinates = path_element.composed_transform()  # type: Transform
        local_transform = path_element.transform
        path_element.transform = transformation_to_absolute_coordinates
        path_element.apply_transform()
        # When converting back to relative coordinates we want to undo everything 
        # except the local transform i.e. the transformations applied directly to element itself
        if local_transform is not None:
            # Before Undo
            # transform to abs = global transforms * local transform
            inverse_local_transform = -local_transform
            transformation_to_absolute_coordinates = transformation_to_absolute_coordinates @ inverse_local_transform
            # After Undo
            # transform to abs = global transforms * local transform * inverse local transform
            #                  = global transforms
            # -> We gave applied them in the forward direction but do not undo them in the backwards direction
            # -> Any transformations applied directly to the element get "backed into" the path itself
        
        transformation_to_relative_coordinates = -transformation_to_absolute_coordinates
        return transformation_to_relative_coordinates

    def _convert_to_relative_coodinates(self, path_element: PathElement, transformation: Transform):
        # Undo the transformation to absolute coordinates
        path_element.transform = transformation
        path_element.apply_transform()

    def _bounds_intersect_visibility(self, bounds: BoundingBox) -> bool:
        x_min1, y_min1 = self.from_transform(bounds.left, bounds.top)
        x_max1, y_max1 = self.from_transform(bounds.right, bounds.bottom)

        x_min2, y_min2 = self.bounds[0]
        x_max2, y_max2 = self.bounds[1]

        # One Rectangle has no area, we ignore this case since lines are relevant
        # if x_min1 == x_max1 or y_min1 == y_max1 or x_min2 == x_max2 or y_min2 == y_max2:
        #    return False

        # One Rectangle is entirely to the side of the other
        if x_min1 > x_max2 or x_min2 > x_max1:
            return False

        # One Rectangle is entirely above the other
        if y_min1 > y_max2 or y_min2 > y_max1:
            return False
        
        return True
    
    def _project(self, x: float, y: float) -> Point:
        longitude, latitude = self.from_transform(x, y)
        longitude, latitude = self.bound_clamp(longitude, latitude)
        return self.to_transform(longitude, latitude)

    def _update_start_coordinates(self, x: float, y: float):
        if self._start_x_untransformed is None:
            self._start_x_untransformed = x
            self._start_y_untransformed = y

    def _transform_move(self, move: Move):
        self._update_start_coordinates(move.x, move.y)
        self._current_x_untransformed = move.x
        self._current_y_untransformed = move.y
        self.transformed_path.append(Move(*self._project(move.x, move.y)))
    
    def _transform_line(self, line: Line):
        line_function = get_line_function((self._current_x_untransformed, self._current_y_untransformed), (line.x, line.y))
        self._transform_basis_function(line_function)

    def _transform_quadratic(self, curve: Quadratic):
        start = (self._current_x_untransformed, self._current_y_untransformed)
        control_a = (curve.x2, curve.y2)
        end = (curve.x3, curve.y3)
        curve_function = get_quadratic_bezier_function(start, control_a, end)
        self._transform_basis_function(curve_function)
        
    def _transform_cubic(self, curve: Curve):
        start = (self._current_x_untransformed, self._current_y_untransformed)
        control_a = (curve.x2, curve.y2)
        control_b = (curve.x3, curve.y3)
        end = (curve.x4, curve.y4)
        curve_function = get_cubic_bezier_function(start, control_a, control_b, end)
        self._transform_basis_function(curve_function)

    def _transform_arc(self, arc: Arc):
        start = (self._current_x_untransformed, self._current_y_untransformed)
        end = (arc.x, arc.y)
        radii = (arc.rx, arc.ry)
        x_angle = arc.x_axis_rotation
        sweep = arc.sweep
        large = arc.large_arc
        arc_function = get_arc_function(start, end, radii, x_angle, large, sweep)
        self._transform_basis_function(arc_function)


    def _transform_basis_function(self, basis_function: Producer):
        def transformed_basis(t: float)-> Point:
            return self._project(*basis_function(t))
        points = self.approximator(transformed_basis)
        for x,y in points:
            self.transformed_path.append(Line(x,y))
        self._current_x_untransformed, self._current_y_untransformed = basis_function(1.0)