# gCode Generator

For my PhD I built a travrse system which could move measurement probes to predefined coordinates. The system was controlled through a repurposed 3D-printer motherboard, which was salvaged from an old [Creality](https://en.wikipedia.org/wiki/Creality) Ender 3. The Python Scripts herein generate gCode which can be transmitted to the motherboard in order to control the motion of the traverse system.

![alt text](https://github.com/hohenhau/pressure_evaluatio/blob/main/_process_diagram.png?raw=true)

## 1. Creating sample points along a line

Multi-Hole Probes are essentially Pitot Tubes with multiple pressure ports. While a Pitot Tube can only estimate the velocity magnitude, the differences in pressure between the ports of a [Multi-Hole Probe](https://www.surreysensors.com/products/digital-seven-hole-probe-system/) allow for the estimation all three velocity components. The script herein is suitable for probes with 5 holes or more.

### 1.1 Multi-Hole Probe Calibration and Interpolation

Usually, Multi-Hole probes are supplied with calibration files. These contain measurements take at a range of different yaw and pitch angles. The increments of the angles are usually too coarse to be used in experiments. It is therefore necessary to use interpolation to artificially increase the resolution and thereby the accuracy of the probe. This interpolation is carried out with the [run_interpolate.py](https://github.com/hohenhau/pressure_evaluation/blob/main/run_interpolate.py) script.

### 1.2 Estimating Velocity Components from Multi-Hole Probe Data

Once the interpolation has been completed, the velocity components can be computed using the [run_multi_hole_velocity.py](https://github.com/hohenhau/pressure_evaluation/blob/main/run_multi_hole_velocity.py) script. If a raw coordinate log file exits, this script will also process sort the locations and durations spent at each location. 


### 1.3 Sorting Velocity Components into Distinct Time Frames or Coordinates

Once the velocities have been estimated, the data can be sorted into specific time frames using [run_multi_hole_time_frames.py](https://github.com/hohenhau/pressure_evaluation/blob/main/run_multi_hole_time_frames.py), or assigned to specific coordinates using [run_multi_hole_field.py](https://github.com/hohenhau/pressure_evaluation/blob/main/run_multi_hole_field.py). Optionally, Coordinate-based data can also be graphed.

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
