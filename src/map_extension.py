from abc import ABC, abstractmethod
import enum
from cartography.projection_builder import ProjectionBuilder
import inkex
from inkex import PathElement, ShapeElement, Group
from cartography.projection import Projection

class MapEffect(inkex.EffectExtension, ABC):
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--precision", type=float, help="The approximator tolerance")
        pars.add_argument("--maximal_resolution", type=int, help="The maximal resolution of the approximator")
        pars.add_argument("--increment", type=int, help="The resolution increment of the approximator")

        pars.add_argument("--z_limit", type=float, help="The minimal z_value that causes a jump fill")
        pars.add_argument("--z_fill", type=int, help="Number of points to fill into a jump")
        

    def create_projection_builder(self, width, height) -> ProjectionBuilder:
        precision = self.options.precision
        maximal_resolution = self.options.maximal_resolution
        increment = self.options.increment
        z_limit = self.options.z_limit
        z_fill = self.options.z_fill

        return ProjectionBuilder()\
                .with_logger(self.msg)\
                .from_equirectangular(width, height)\
                .with_equidistant_approximator(precision, maximal_resolution, increment, z_limit, z_fill)           

    def effect(self):
        width, height = self.svg.viewport_width, self.svg.viewport_height  
        width, height = self.svg.unittouu(width), self.svg.unittouu(height)
        
        builder = self.create_projection_builder(width, height)
        projection = self.get_projection(builder, width, height)

        for elem in self.svg.selection:
            elem_copy = elem.copy()
            if isinstance(elem_copy, ShapeElement) and not isinstance(elem_copy, Group):
                elem_copy = elem_copy.to_path_element()
            if elem.label is not None:
                elem_copy.label = elem.label +"_projection"
            else:
                elem_copy.set_id(elem.get_id()+"_projection")
            
            elem.getparent().add(elem_copy)
            self.apply_projection(elem_copy, projection)
    
    @abstractmethod
    def get_projection(self, projection_builder: ProjectionBuilder, width: float, height: float) -> Projection:
        pass

    def apply_projection(self, element, projection: Projection):
        if isinstance(element, PathElement):
            projection.transform(element)
        elif isinstance(element, ShapeElement) and not isinstance(element, Group):
            # Convert element to path
            element.composed_transform()
            path = element.to_path_element()
            parent = element.getparent()
            found_index = None
            for index, child in enumerate(parent):
                if child == element:
                    found_index = index
                    break
            parent[found_index] = path
            projection.transform(path)
        
        # Recursion
        for elem in element:
            self.apply_projection(elem, projection)
