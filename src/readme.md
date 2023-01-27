# About the implementation
The goal of the project is to convert between map projections in inkscape.

## Code Structure
The entrypoint for all extensions is `map_extension.py`. It contains the `MapEffect` base class that is extended by every map projection. Every `MapEffect` first creates a `ProjectionBuilder` - a simple builder pattern - to configure the `Projection` which implements the actual transformation.

When the `MapEffect.effect` method is executed we 
1. fetch the `Projection` from the `ProjectionBuilder`
2. iterate over our selection and duplicate all elements
3. convert all `ShapeElement`s to paths
4. apply `Projection.transform` to all paths

In `Projection.transform` we then go through the individual SVG path steps and transform them one-by-one.

## The Transformation in Theory
To start it helps to think of a map projection as a function that transforms a given longitude and latitude to a specific x,y coodinate. To transform a map from map projection A (e.g. Equirectangular) to map projection B (e.g. Mercator) means we first apply the inverse of the projection A - therby converting the map back into the longitude and latitude space before then applying projection B.
In our example this would mean we'd have to first undo the equirectangular projection before we could apply mercator.

In actuallity we first start out by interpreting our path as a lists of function `f(t)` which maps each `t` to a x,y coordinate. For example a path consisting of a line, and a bezier curve. We can get the data for those from the actual SVG path and then construct the function in the `basis_function.py`. So if we have a line segment from (0,0) to (100,20) we would call `get_line_function((0,0), (100,20))` which would return a function `f(t)` with `f(0) = (0,0)` and `f(1)=(100,20)`. This function represents our path in the "old projection" (i.e. equirectangular). Next we apply the inverse of the equirectangular lets call it`equi_inv(x,y)` which returns the longitude and latitude for every x,y coordinate. By composing these two functions to `equi_inv(f(t))` we get the path transformed to the longitude, latitude space. Lastly we need to transform the path to our new projection for that we need a function `merca(long,lat)` which transforms any longitude, latitude pair to a x,y coordinate in the new projection. Composing everything we get `transformed_path(t)= merca(equi_inv(f(t)))` a function that takes in t, and returns the x,y coordinate in the new projection.

Once we have our `transformed_path(t)` all we have to do is actually create a path following this function. Sadly this isn't as easy as simply changing the parameters of the input path. That is because what was a line in the orignal projection might no longer be a line in the new projection. Think for example of the parallels in an equirectangular map, that turn into circles in a stereographic projection. For this reason we approximate our function.
We sample several points from our `transformed_path(t)` and create a piecewise-linear approximation. Basicly we put in several values for `t` and draw lines between the resulting x,y coordinates. This will obviously not a perfect curve. But given a sufficent number of line segments the difference wont be visible (like with a 60-sided polygon and a circle). 

## In Code
The actual transformations can be found in `cartography.transformations`. Here we have `inverse_map_transformation.py` implementing the inverse tranforms that are applied first. We also have `map_transform.py` where you can find the "regular" forward transformations. Some of the more involved transformations like Robinson or Peirce Quincuncial also have additional files to aid with readability. Latsly we have `generic_transformation.py` which contains some additional functions like linear transformations which are often reused for the implementation of the transformations.

The code implementing the linear approximations can be found in `approximator.py`. The approximator function takes in a "producer" (like our `transformed_path(t)`), lower and upper bounds, and a precision / number of points and retuns a list of points between the provided bounds.