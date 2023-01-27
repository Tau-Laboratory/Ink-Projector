from typing import  List
from cartography.projection_types import Approximator, Producer,Point
import numpy as np


# Equidistant Approximation

def get_equidistant_approximator(precision: float, maximal_resolution: int, increment: int, z_limit: float, z_fill: int) -> Approximator:
    """
    Returns a preconfigured equidistant approximator with the given parameters for the intervall [0,1]
    """
    def approximator(function: Producer)-> List[Point]:
        return equidistant_approximation(function, 0.0, 1.0, precision, increment, maximal_resolution, z_limit, z_fill)
    return approximator

def equidistant_approximation(function: Producer, lower_bound: float, upper_bound: float, precision: float, increment=1, maximal_resolution=35, z_limit=0.0, z_fill=4):
    """
    Takes in a function and a lower and upper bound.
    It returns a list of points that are the results of evaluating the function between those bounds.
    If z_limit is <=0.0 it just uniformly samples points from the given interval until the picewise linear
    approximation differs lass then the provided precision from the given function. This is checked by
    sampling the midpoints between the sampled points.
    Additionally there is a maximal resolution determining the maximal number of points regardless of the precision.
    Should the z_limit be greater than 0.0 after this sample step we do an additional z filling step:
    
    Here we take the distances between the sampled points and compute their z-score ( Sample  - Sample Mean ) / Sample Standard Diviation
    This gives us the samples "unusuallity" in units of standard diviation.
    Any jump between points that is unusual as determined by exceeding the z limit will cause a z-fill.
    A z-fill inserts additional points evenly spaced in the unusual gap. The number of points is determined by the z_fill parameter.
    """
    
    maximal_resolution = max(2, maximal_resolution)
    resolution = 2
    length = upper_bound - lower_bound
    
    found_imprecision = False
    points = []

    while resolution < maximal_resolution:
        point_count = resolution - 1 
        # Compute a list of evenly spaced points between the bounds
        points = [function(lower_bound + length*(float(i)/point_count)) for i in range(point_count+1)]
        # Compute the midpoints between the evenly spaced points
        mid_points = [function(lower_bound + length*(float(2*i+1)/(2*point_count))) for i in range(point_count)]
        found_imprecision = False
        for i in range(point_count):
            # Check if any of those midpoints differs more than the acceptable margin from its linear approximation
            mid_value = mid_points[i]
            mid_approximation = np.add(np.array(points[i]), np.array(points[i+1])) / np.array(2)
            error = np.linalg.norm(np.array(mid_value) - mid_approximation)
            if error > precision:
                # We found a midpoint that differs too much => We must increase the resolution
                found_imprecision = True
                break
        if not found_imprecision:
            # All midpoints are sufficently approximated
            break
        resolution += increment

    if found_imprecision:
        # Even the closest approximation was not enough, we use the maximal resolution as a last resort
        points = [function(lower_bound + length*(float(i)/(maximal_resolution-1))) for i in range(maximal_resolution)]

    # Z Score Filling
    # Uses the z-score https://en.wikipedia.org/wiki/Standard_score
    # Find unusual jumps in the data that are potential discontinuities of the function
    # then add additional points around these jumps to improve the quality around those jumps
    if z_limit > 0.0 and len(points) > 1:
        # Compute the pairwise distance between the sampled points
        distances = np.linalg.norm(np.diff(points, axis=0), axis=1)
        # Compute the mean and the standard deviation of those distances
        mean = np.mean(distances)
        std = np.std(distances)
        if std == 0.0:
            return points
        # Compute the z values of those distances
        # The z value can be thought of as the distance between the sample and the mean in units of standard deviation
        # i.e. a z value of 1.4 means the sample is 1.4 standard deviations away from the mean
        z_values = np.abs((distances - mean) / std)

        resolution = len(z_values)
        fill_distance = 1/ ((1+z_fill)*resolution) 
        # Go though each distance 
        # reversed order since we may insert additional points and that helps keeping the indices straight
        for i in reversed(range(len(z_values))):     
            if z_values[i] > z_limit:
                # We found a jump that is unusual => We fill in additional points in the jump
                # This is a dynamic increase of resolution at unusual points
                start = i/resolution
                added_points = [function(start + (j+1) * fill_distance) for j in range(z_fill)]
                points[i+1:i+1] = added_points
    return points 

# -----------------------------------------------------------------------------------------------
# Dynamic linear apprximation
# Currently unused due to poor performance with some projections

def get_linear_approximator(precision: float) -> Approximator:
    def approximator(function: Producer)-> List[Point]:
        return linear_approximation(function, 0.0, 1.0, precision)
    return approximator

def linear_approximation_recursive(function: Producer, lower_bound: float, upper_bound: float, precision: float)-> List[Point]:
    # compute f(low), f(high), f(mid)
    f_low = function(lower_bound)
    f_heigh = function(upper_bound)

    midpoint = (upper_bound + lower_bound) / 2
    f_mid = np.array(function(midpoint))
    
    # compute approximation a(mid) = (f(low) + f(high))/2
    midpoint_approximation = np.add(np.array(f_low), np.array(f_heigh)) / np.array(2)
    
    # compute error ||a(mid) - f(mid)||
    error = np.linalg.norm(f_mid - midpoint_approximation)

    if error < precision:
        return [f_low, f_heigh]
    # if error < precision
    # return f(low), f(heigh)
    # otherwise
    lower_half = linear_approximation_recursive(function, lower_bound, midpoint, precision)
    upper_half = linear_approximation_recursive(function, midpoint, upper_bound, precision)

    # return a(low),...,a(mid),...,a(heigh)
    # remove the duplicate midpoint
    return lower_half[:-1] + upper_half

def linear_approximation(function: Producer, lower_bound: float, upper_bound: float, precision: float, max_depth=14) -> List[Point]:
    """
    Start with line l: f(0) -> f(1)
    Check if ||f(0.5)-l(0.5)|| > p
    If so Split line into two lines l1: f(0) -> f(0.5), l2: f(0.5) -> f(1)
    Repeat
    """
    # The current lower bound and lower value of our line
    low_bound = lower_bound
    low_value = function(low_bound)

    # The list of higher bounds and values and our worklist
    high_entries = [(upper_bound, function(upper_bound))]
    # The output list
    points = [low_value]
    while len(high_entries) > 0:
        high_bound, high_value = high_entries[-1]
        # Compute the midpoint of our current low and high
        mid_bound = (low_bound + high_bound) / 2
        mid_value = function(mid_bound)
        mid_approximation = np.add(np.array(low_value), np.array(high_value)) / np.array(2)
        error = np.linalg.norm(np.array(mid_value) - mid_approximation)
        # Check if the midpoint is sufficently approximated by the current line
        if error > precision and len(high_entries) <= max_depth:
            # if not add the midpoint as the new high value
            # => We must increase the resolution
            high_entries.append((mid_bound, mid_value))
        else:
            # Otherwise we are done with this line segment, we remove the high value
            # and set the low value to this old high value
            # => We Decrease Resolution
            low_bound, low_value = high_entries.pop()
            points.append(low_value)
    return points
