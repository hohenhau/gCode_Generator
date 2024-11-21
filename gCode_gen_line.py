# Script to generate gcode file for probe traverse mechanism

import numpy as np                  # import numpy module
import matplotlib.pyplot as plt     # import plot module

# Specify base parameters and geometry

sample_time = 5                 # wait time in seconds
buffer_start = 1.5              # pre-sample buffer
buffer_end = 1.5                # post-sample buffer

start_x = 10                    # initial x coordinate in relation to origin
end_x = 290                     # final x coordinate in relation to origin
start_z = 10                    # initial z coordinate in relation to origin
end_z = 290                     # final z coordinate in relation to origin
points = 100                    # number of measurement points

origin_x = 0                   # calibrated starting position for x
origin_z = 0                   # calibrated starting position for z

max_tilt_x = 0                  # tilt in the x direction
max_tilt_z = 0                  # tilt i the z direction

traverse_max_x = 700            # maximum horizontal travel
traverse_max_z = 820            # maximum vertical travel


# calculate bounds of test grid

def generate_test_grid(points, start_p, end_p, origin_p, tilt_p):

    array_display = np.linspace(start_p, end_p, points)  # create an array with equally spaced points
    array_offset = np.array(list()).astype(float)
    array_move = np.array(list()).astype(float)
    array_tilt = np.array(list()).astype(float)

    for count, coordinate in enumerate(array_display):

        tilt = round(tilt_p * (count / (points - 1)), 2)

        """
        if start_p < end_p:
            tilt = round(tilt_p * (count / (points - 1)), 2)
        else:
            tilt = round(tilt_p * (1 - (count / (points - 1))), 2)
        """

        array_tilt = np.append(array_tilt, coordinate + tilt)
        array_offset = np.append(array_offset, coordinate + origin_p)
        array_move = np.append(array_move, coordinate + tilt + origin_p)

    min_p = np.amin(array_move)
    max_p = np.amax(array_move)

    return array_display, array_tilt, array_offset, array_move, min_p, max_p


x_display, x_tilt, x_offset, x_move, min_x, max_x = generate_test_grid(points, start_x, end_x, origin_x, max_tilt_x)
z_display, z_tilt, z_offset, z_move, min_z, max_z = generate_test_grid(points, start_z, end_z, origin_z, max_tilt_z)


# basic geometry checks and creation of arrays

if end_x > traverse_max_x:                                  # check that the traverse can reach all points in x
    print("traverse is too small in x direction")           # print error message if points are unreachable
    exit()
elif end_z > traverse_max_z:                                # check that the traverse can reach all points in z
    print("traverse is too small in z direction")           # print error message if points are unreachable
    exit()
else:                                                       # continue if all points can be reached
    print("bounds are within range")                        # print success message


# create coordinate array
xz_move = np.stack((x_move, z_move), axis=1)
xz_offset = np.stack((x_offset, z_offset), axis=1)
xz_tilt = np.stack((x_tilt, z_tilt), axis=1)
xz_display = np.stack((x_display, z_display), axis=1)

# graph the grid
plt.scatter(xz_tilt[:, 0], xz_tilt[:, 1], alpha=0.5)
plt.show()

# created and write data points to gcode file

file_name = str(f"{points}points_start({start_x}|{start_z})_end({end_x}|{end_z})")
wait_time = sample_time + buffer_start + buffer_end               # wait time in seconds

with open(f'/Users/alex/Desktop/{file_name}.gcode', 'w') as file:

    file.write(';gcode file for traversing probe  \n \n')                   # header of gcode file
    file.write('M111 S0 \t\t\t\t; disable debug mode \n')                   # disable debug mode
    # file.write('M111 S2 \t\t\t\t; enter debug mode \n')                     # enter debug mode
    file.write('M302 S0 \t\t\t\t; Allow cold extrusion \n')                 # line to allow cold extrusion
    file.write('M106 S0 \t\t\t\t; Turn-off fan \n')                         # line to disable fan
    file.write('M104 S0 \t\t\t\t; Turn-off hotend \n')                      # line to disable hotend
    file.write('M140 S0 \t\t\t\t; Turn-off bed  \n')                        # line to disable bed
    file.write('G90 \t\t\t\t; Absolute positioning \n')                     # enter into absolute position mode
    file.write('M75 \t\t\t\t; start timer \n')                              # start timer
    file.write('G28 \t\t\t\t; Home \n')                                     # calibrate homeing position
    file.write('M204 S500 \t\t\t; set default acceleration \n')             # set default acceleration
    file.write('M205 X8 Y8z \t\t\t; advanced setting to set jerk  \n')      # set default jerk
    file.write('M205 X8 Y8z \t\t\t; advanced setting to set jerk  \n')              # set default jerk
    file.write(f'G4 P{2000} \t\t\t; wait time (milliseconds \n')                    # Wait specified time
    file.write(f'sampling time = {wait_time} \t\t; report wait time \n')            # report wait time
    file.write(f'origin x = {origin_x} \t\t\t; report test margin\n')               # report test origin
    file.write(f'origin z = {origin_z} \t\t\t; report test margin \n')              # report test origin
    file.write(f'start x = {start_x} \t\t\t; report test margin\n')                 # report test start
    file.write(f'start z = {start_z} \t\t\t; report test margin \n')                # report test start
    file.write(f'end x = {end_x} \t\t\t; report test margin\n')                     # report test end
    file.write(f'end z = {end_z} \t\t\t; report test margin \n')                    # report test end
    file.write(f'points = {points} \t\t\t; report point number \n')                 # report number of points in x
    file.write(f'tilt x = {max_tilt_x} \t\t\t; report point distribution \n')       # report tilt in x
    file.write(f'tilt z = {max_tilt_z} \t\t\t; report point distribution \n')       # report tilt in z
    file.write(f'G1 X{round(xz_move[0][0], 2)} F20000\t\t\t; move to initial X\n')  # move to initial X
    file.write(f'G1 Z{origin_z + start_z} F20000\t\t\t; move to initial Z\n')       # move to initial Z


    for i in zip(xz_move, xz_display):

        x_i = round(i[0][0], 2)
        z_i = round(i[0][1], 2)
        x_j = round(i[1][0], 2)
        z_j = round(i[1][1], 2)

        file.write(f'G1 X{x_i} Z{z_i} F20000\t\t; movement\n')                      # specify coordinates and speed
        file.write(f'G4 P10 \t\t\t\t; wait time (milliseconds \n')                  # Wait specified time
        file.write(f'M31 \t\t\t\t; report time \n')                                 # report time
        file.write(f'X = {x_j}, Z = {z_j} \t\t; report position \n')                # report current position
        # file.write(f'M114_DETAIL D \t\t\t; report current position \n')           # report position (not working)
        file.write(f'G4 P{wait_time * 1000} \t\t\t; wait time (milliseconds \n')    # Wait specified time

    # file.write(f'G1 X{round(xz_move[0][0], 2)} Z{origin_z + start_z} F20000\t\t; move to point\n')  # move to point
    file.write(f'G1 Z{1} F20000\t\t\t; return to start Z\n')                            # return to start Z
    file.write(f'G1 X{1} F5000\t\t\t; return to start X\n')                             # return to start X
    file.write('\n\n;end of gcode')                                                     # gcode end line

print("gcode file has been created")                                                    # print success to terminal

# end of code
