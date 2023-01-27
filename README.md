# Ink-Projector
An inkscape plugin for automatic map projection


# About the Project
The goal of Ink-Projector is to transform maps drawn in Inkscape to be automatically converted between map projections.For example from an equirectangular map to a mercator projection or a stereographic projection. This should be done by directly transforming the paths themselfs without having to manually retrace anything.

# Installation
The plugin is installed by downloading the code as a zip and extracting it in the plug-in folder of your installation of Inkscape. You can find this folder by checking `Edit > Preferences > System: User extensions` in Inkscape.

Once you have copied the folder and restarted Inkscape your `Extension` menu should now have a `Cartography` submenu. If you do you've installed the plug-in successfully. 

# Using the Plugin
1. Select any group or elements that you want to project. the easiest way is to have a group containing all you map elements and simply select this group.
2. Select the transformation you want to apply from the `Cartography` menu.
3. Configure your projection (more on that below).
4. Click Apply
5. Give it some time. Depending on the size and complexity of your map it might take a couple of minutes or even freeze your Inkscape for a bit... It happens... Sorry...
6. Once it is done you should now have two versions of your map: The original and a projected copy. (Note: The projection process never affects the original, all transformations are applied to the copy) 

# Configuring your Projection
Depending on the projection you have choosen there might be two types of configurations
## 1. Projection Specific Options
Here you can find some options to configure the projection you have choosen usually this involves picking standard lattitiudes or similar information. All angles are in degrees.


## 2. Approximator Options
Every projection has so calles `Approximator` options. These dictate how the mathmatical formular of the projection should be converted back into points and lines on the canvas. Probably the most important two are `Tolerance` and `Maximal Resolution` These two decide the quality of your output.

To understand this, a bit of a background on the behind the scenes: Your map probably consists of a bunch of shapes made up from lines and curve. What the extension does is interpret each of those lines and curves as a formular and then apply a bunch of math to in in order to get a new formular for the projected "line". The "line" is in quotes since what may have started as a line might become something that is not a line after the projection (think the parallels of latitude that become circles in a stereographic projection). In the end the extension has to convert this formular back into lines. So we have to do some level of approximation: So we approximate each curve with a bunch of lines. The `Tolerance` options states how much the line is allowed to deviate form the mathmatical ideal curve. The bigger it is the more "jagged" your approximation. The smaller you make it the more precise. This comes at a cost, for high precision we have to add a lot of new points which will take some time. 
Additionaly we limit the total number of points with the option `Maximal Resolution`. This options tells you how many points the extension is allowed to use to appoximate each part of the curve. For example value of 35 would mean that each segment could be approximated by up to 35 points (i.e. 34 Line Segments). So if you had a map consisting of 100 Line Segments the projection is allowed to have up to 3400 Line Segments. Usually it will be a lot fewer since most lines in the original will also be lines in the projeciton.
If you think your result looks too jagged try increasing the maximal resolution and reducing the tolerance.

`Resolution Increment` is mostly a performance option. It dictates how much the resolution should be increased if the tolerance is of. So if we find a place where the approximation differs by more than  the tolerance we add a number of points dictated by the increment. Usually 1 is fine. But if you find you have a map that comes out with a lot of complex shapes a higher number might make your projection faster.

Next up we have the `z Limit` and `z Fill` options. Unfortunately these will require another dive into the background:
Most projections are pretty continuus, meaning points that are close together in the original are also quite close toghether in the projection but there are some projections (for example `Peirce Quincuncial`) where this is not the case. The map might be cut though the middle. This might result in some very uggly jumps and line artifacts. You could try and fix them by upping the resolution and reducing the tolerance. But there is also another option: Z Filling.

If you enable Z Filling by picking a `z Limit` above 0.0 the extension will try to find and fix these kinds of issues. The `z Limit` is anolagous to the `Precision` from before: The smaller the faster it identifies something as an unwanted artifact and add additional points in this gap to fix the artifact. The `z Fill` gives the number of points that should be added into these gaps. A value of 4 would mean four additional points for every jump the system has identified.

With all these options you can just play around, or - if your map is simple in its design - try the preview and see how each option is affecting the result. If you have a complex map you can draw a quick sketch of your map and test the projeciton on that sketch before you commit to the full map.

# Troubleshooting
## Performance Issues
Unfortunately this extension is not the most efficent. Especially for very complex and detailed maps it might take quite a while or even freeze Inkscape. Usually it unfreezes after a while but it is still annoying. What you could do to avoid this is transform you map layer-by-layer or even path-by-path. That way each projection should finish quicker. 

## Any Other issues
There may be still some bugs in there. I have tested it and all its components I do make misstakes. Should you find any let me know and I see what I can do.

# Licence
All the code is licenced under a GPL-2 licence unless explicitly stated otherwise at the code.