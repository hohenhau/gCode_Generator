# Script to generate gcode file for probe traverse mechanism

import numpy as np          # import numpy module

# Specify base parameters and geometry

length_x = 280              # horizontal extent of measured section
length_z = 280              # vertical extent of measured section
margin_x = 10                # horizontal clearance
margin_z = 10                # vertical clearance
points_x = 10               # number of horizontal points
points_z = 10               # number of vertical points
wait_time = 20              # wait time in seconds

start_x = 0                # calibrated starting position for x
start_z = 0                # calibrated starting position for z


traverse_max_x = 700        # maximum horizontal travel
traverse_max_z = 820        # maximum vertical travel


# calculate bounds of test grid

if points_x == 1:                                           # centre points horizontally if there is only x array
    min_x = start_x + (length_x - margin_x * 2) / 2         # calculate position of centre
    max_x = min_x                                           # as there is only one point, min and max are equal
else:                                                       # if there are multiple points in x
    min_x = start_x + margin_x                              # calculate minimum boundary for x
    max_x = start_x + length_x - margin_x * 2               # calculate maximum boundary for x

if points_z == 1:                                           # centre points vertically if there is only z array
    min_z = start_z + (length_z - margin_z * 2) / 2         # calculate position of centre
    max_z = min_z                                           # as there is only one point, min and max are equal
else:                                                       # if there are multiple points in z
    min_z = start_z + margin_z                              # calculate minimum boundary for z
    max_z = start_z + length_z - margin_z * 2               # calculate maximum boundary for z


# basic geometry checks and creation of arrays

if max_x > traverse_max_x:                                  # check that the traverse can reach all points in x
    print("traverse is too small in x direction")           # print error message if points are unreachable
elif max_z > traverse_max_z:                                # check that the traverse can reach all points in z
    print("traverse is too small in y direction")           # print error message if points are unreachable
else:                                                       # continue if all points can be reached
    print("bounds are within range")                        # print success message

array_x = np.linspace(min_x, max_x, points_x)                   # create an array with equally spaced x coordinates
array_z = np.linspace(min_z, max_z, points_z)                   # create an array with equally spaced z coordinates
array_xz = np.array([[[0.0, 0.0]] * points_x] * points_z)       # create array which will contain x and z coordinates

for i_z in range(len(array_z)):                                 # create xy coordinate raster
    for i_x in range(len(array_x)):
        array_xz[i_z][i_x][0] = round(float(array_x[i_x]), 2)   # populate raster with x coordinates
        array_xz[i_z][i_x][1] = round(float(array_z[i_z]), 2)   # populate raster with z coordinates


# created and write data points to gcode file

with open(f'/Users/alex/Desktop/{length_x}x{length_z}mm_{points_x}x{points_z}pts.gcode', 'w') as file:

    file.write(';gcode file for traversing probe  \n \n')                   # header of gcode file
    file.write('M111 S0 \t\t\t\t; disable debug mode \n')                   # disable debug mode
    # file.write('M111 S2 \t\t\t\t; enter debug mode \n')                     # enter debug mode
    file.write('M106 S0 \t\t\t\t; Turn-off fan \n')                         # line to disable fan
    file.write('M104 S0 \t\t\t\t; Turn-off hotend \n')                      # line to disable hotend
    file.write('M140 S0 \t\t\t\t; Turn-off bed  \n')                        # line to disable bed
    file.write('G90 \t\t\t\t; Absolute positioning \n')                     # enter into absolute position mode
    file.write('M75 \t\t\t\t; start timer \n')                              # start timer
    file.write('G28 \t\t\t\t; Home \n')                                     # calibrate homeing position
    file.write('M204 S500 \t\t\t; set default acceleration \n')             # set default acceleration
    file.write('M205 X8 Y8z \t\t\t; advanced setting to set jerk  \n')      # set default jerk
    file.write('M205 X8 Y8z \t\t\t; advanced setting to set jerk  \n')  # set default jerk
    file.write(f'G4 P{wait_time * 1000} \t\t\t; wait time (milliseconds \n')    # Wait specified time
    file.write(f'sampling time = {wait_time} \t\t; report wait time \n')  # report current position

    for i_0 in array_xz:
        for i_1 in i_0:

            x_show = round(i_1[0] - start_x, 2)                                         # calculate relative x position
            z_show = round(i_1[1] - start_z, 2)                                         # calculate relative z position

            file.write(f'G1 X{i_1[0]} Z{i_1[1]} F20000\t\t; movement\n')                # specify coordinates and speed
            file.write(f'G4 P10 \t\t\t\t; wait time (milliseconds \n')                  # Wait specified time
            file.write(f'M31 \t\t\t\t; report time \n')                                 # report time
            file.write(f'X = {x_show}, Z = {z_show} \t\t; report position \n')        # report current position
            # file.write(f'M114_DETAIL D \t\t\t; report current position \n')           # report position (not working)
            file.write(f'G4 P{wait_time * 1000} \t\t\t; wait time (milliseconds \n')    # Wait specified time

    file.write('\n\n;end of gcode')                                                     # gcode end line

print("gcode file has been created")                                                    # print success to terminal

# end of code
