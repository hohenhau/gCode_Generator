# gCode Generator

For my PhD I built a travrse system which could move measurement probes to predefined coordinates. The system was controlled through a repurposed 3D-printer motherboard, which was salvaged from an old [Creality](https://en.wikipedia.org/wiki/Creality) Ender 3. The Python Scripts herein generate gCode which can be transmitted to the motherboard in order to control the motion of the traverse system.

## 1. Creating sample points along a line

Create coordinates along a line is achieved with the [gCode_gen_line.py](https://github.com/hohenhau/gCode_Generator/blob/main/gCode_gen_line.py) script. The line is defined through a start and end point and the number of points in between. The result is a set of coordinates along a line:

![alt text](https://github.com/hohenhau/gCode_Generator/blob/main/coordinates_line.png)

## 2. Creating Sample Points Over a Grid

### 2.1 Regular Grids

To create a regular grid of coordinates, one can use the [gCode_gen_regular.py](https://github.com/hohenhau/gCode_Generator/blob/main/gCode_gen_regular.py) or the [gCode_gen_irregular.py](https://github.com/hohenhau/gCode_Generator/blob/main/gCode_gen_irregular.py) scripts. Using the latter to create a regular grid requires setting all tilt and growth parameters to 0. The result is a regular grid:

![alt text](https://github.com/hohenhau/gCode_Generator/blob/main/coordinates_grid_regular.png)

### 2.2 Tilted Grids

If the grid system needs to line up with a test section with edges that are non-perpendicular, it is possible to skew the coordinate system. This is achieved using the [gCode_gen_irregular.py](https://github.com/hohenhau/gCode_Generator/blob/main/gCode_gen_irregular.py) script and changing the tilt parameters. The result is a skewed grid:

![alt text](https://github.com/hohenhau/gCode_Generator/blob/main/coordinates_grid_tilted.png)

### 2.3 Irregular Grids

In certain cases it might be beneficial to create irregular grids, which are more dense towards the edges, in order to more accurately capture the boundary layer of flow. This is achieved using the [gCode_gen_irregular.py](https://github.com/hohenhau/gCode_Generator/blob/main/gCode_gen_irregular.py) script and changing the growth parameters. The result is an irregular grid:

![alt text](https://github.com/hohenhau/gCode_Generator/blob/main/coordinates_grid_irregular.png)
