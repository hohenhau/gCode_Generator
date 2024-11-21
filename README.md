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

## 2. Creating Sample Points along a grid

A [Pitot Rake](https://www.surreysensors.com/products/amprobes/) is simply a series of Pitot Tubes, and is used for a simple and rapid measurement of the flow field. 

### 2.1 Regular Grids

Using the dynamic pressure measured by the rake, the velocity can easily be calculated using the [run_pitot_rake_velocity.py](https://github.com/hohenhau/pressure_evaluation/blob/main/run_pitot_rake_velocity.py) script. 

### 2.2 Tilted Grids

Using the [rgCode_gen_irregular.py](https://github.com/hohenhau/gCode_Generator/blob/main/gCode_gen_irregular.py) and changing the tilt parameters, it is possible to generate a skewed grid. This is particularly useful, if the measured grid needs to line up with a test section that is not perfectly perpendicular.
![alt text](https://github.com/hohenhau/gCode_Generator/blob/main/coordinates_grid_tilted.png)

## 3. Irregular Grids

asdf
### 3.1 Sorting Static Pressures into Distinct Time Frames

Using the [rgCode_gen_irregular.py](https://github.com/hohenhau/gCode_Generator/blob/main/gCode_gen_irregular.py) script, the static pressure measurements can be assigned to specific user-defined time frames at and wind tunnel locations.
