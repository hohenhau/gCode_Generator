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

points_x = 21                    # number of measurement points
points_z = 21                   # number of measurement points

origin_x = 0                    # calibrated starting position for x
origin_z = 0                    # calibrated starting position for z

max_x_tilt = 0                  # tilt in the x direction
max_z_tilt = 0                  # tilt i the z direction

traverse_max_x = 700            # maximum horizontal travel
traverse_max_z = 820            # maximum vertical travel


# specify if points should be more concentrated towards the edges

concentrate_x_min = False
concentrate_x_max = False
concentrate_z_min = False
concentrate_z_max = False
growth_x = 1.2
growth_z = 1.2


# check if concentration settings work

def geometry_checker(var, concentrate_min, concentrate_max, growth, points):

    if any([concentrate_min, concentrate_max]) and growth <= 1:
        print(f"growth in {var} has to be greater than 1")
        exit()

    if concentrate_min is True and concentrate_max is True and points % 2 == 0:
        print(f"if minimum and maximum points are to be concentrated, number of {var} points needs to be odd")
        exit()
    elif concentrate_min is True and concentrate_max is True and points < 4:
        print(f"if minimum and maximum points are to be concentrated, number of {var} points needs to be at least 5")
        exit()
    elif concentrate_min is True and points < 3:
        print(f"if minimum points are to be concentrated, number of {var} points needs to be at least 3")
        exit()
    elif concentrate_x_max is True and points_x < 3:
        print(f"if maximum points are to be concentrated, number of {var} pointed needs to be at least 3")
        exit()


geometry_checker("x", concentrate_x_min, concentrate_x_max, growth_x, points_x)
geometry_checker("z", concentrate_z_min, concentrate_z_max, growth_z, points_z)


# calculate bounds of test grid

def generate_test_grid(concentrate_min, concentrate_max, growth, points, start, end):

    range_p = end - start

    if points == 1:                                           # centre points horizontally if there is only  array
        array = list([(end-start)/2])

    elif concentrate_min is False and concentrate_max is False:
        array = np.linspace(start, end, points)                 # create an array with equally spaced points

    elif concentrate_min is True and concentrate_max is True:
        gaps = int(points / 2 + 0.5 - 1)
        max_p = range_p / 2
        initial_spacing = max_p / ((1 - growth ** gaps) / (1 - growth))
        array = np.array(list())
        array = np.append(array, max_p)
        for n in range(gaps):
            spacing = initial_spacing * growth ** n
            next_p = round(array[-1] - spacing, 2)
            array = np.append(array, next_p)
        array = np.append(array, np.sort(array[0:-1]) * -1)       # mirrors array across axis
        array = np.sort(array + max_p + start)

    elif concentrate_min is True or concentrate_max is True:
        gaps = points - 1
        initial_spacing = end / ((1 - growth ** gaps) / (1 - growth))
        array = np.array(list())
        array = np.append(array, end)
        for n in range(gaps):
            spacing = initial_spacing * growth ** n
            next_p = round(array[-1] - spacing, 2)
            array = np.append(array, next_p)
        if concentrate_min is True:
            array = np.sort(array * -1) + start + end
        else:
            array = np.sort(array) + start

    return array, range_p


x_display, range_x = generate_test_grid(concentrate_x_min, concentrate_x_max, growth_x, points_x, start_x, end_x)
z_display, range_z = generate_test_grid(concentrate_z_min, concentrate_z_max, growth_z, points_z, start_z, end_z)

x_display, z_display = np.meshgrid(x_display, z_display)
xz_display = np.stack([x_display.ravel(), z_display.ravel()], axis=1)

add_tilt = list()
for x, z in xz_display:
    x_tilt_local = max_x_tilt * (1 - (end_z - z) / range_z)
    z_tilt_local = max_z_tilt * (1 - (end_x - x) / range_x)
    add_tilt.append([x_tilt_local, z_tilt_local])
add_tilt = np.array(add_tilt)

xz_offset = xz_display + [origin_x, origin_z]
xz_tilt = xz_display + add_tilt
xz_move = xz_display + add_tilt + [origin_x, origin_z]


# basic geometry checks and creation of arrays

max_x = np.amax(xz_move[:, 0])
max_z = np.amax(xz_move[:, 1])

if max_x > traverse_max_x:                                  # check that the traverse can reach all points in x
    print("traverse is too small in x direction")           # print error message if points are unreachable
    exit()
elif max_z > traverse_max_z:                                # check that the traverse can reach all points in z
    print("traverse is too small in y direction")           # print error message if points are unreachable
    exit()
else:                                                       # continue if all points can be reached
    print("bounds are within range")                        # print success message

# graph the grid
plt.scatter(xz_tilt[:, 0], xz_tilt[:, 1], alpha=0.5)
plt.show()

# created and write data points to gcode file

growth_x_str = str(growth_x).replace(".", "-")
growth_z_str = str(growth_z).replace(".", "-")

file_name = str(f"{range_x}x{range_z}mm_{points_x}x{points_z}pts_{growth_x_str}x{growth_z_str}growth")
wait_time = sample_time + buffer_start + buffer_end               # wait time in seconds

with open(f'/Users/alex/Desktop/{file_name}.gcode', 'w') as file:

    file.write(';gcode file for traversing probe  \n \n')                   # header of gcode file
    file.write('M111 S0 \t\t\t\t; disable debug mode \n')                   # disable debug mode
    # file.write('M111 S2 \t\t\t\t; enter debug mode \n')                   # enter debug mode
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
    file.write(f'points x = {points_x} \t\t\t; report point number \n')             # report number of points in x
    file.write(f'points z = {points_z} \t\t\t; report point number \n')             # report number of points in z
    file.write(f'growth x = {growth_x} \t\t\t; report point distribution \n')       # report stretch in x
    file.write(f'growth z = {growth_z} \t\t\t; report point distribution \n')       # report stretch in z
    file.write(f'tilt x = {max_x_tilt} \t\t\t; report point distribution \n')       # report tilt in x
    file.write(f'tilt z = {max_z_tilt} \t\t\t; report point distribution \n')       # report tilt in z
    file.write(f'G1 X{xz_move[0][0]} F20000\t\t\t; move to initial X\n')            # move to initial X
    file.write(f'G1 Z{origin_z + start_z} F20000\t\t\t; move to initial Z\n')       # move to initial Z

    for i in zip(xz_move, xz_display):

        x_i = round(i[0][0], 2)
        z_i = round(i[0][1], 2)
        x_j = round(i[1][0], 2)
        z_j = round(i[1][1], 2)

        file.write(f'G1 X{x_i} Z{z_i} F20000\t\t; movement\n')                      # specify coordinates and speed
        file.write(f'G4 P10 \t\t\t\t; wait time (milliseconds \n')                  # Wait specified time
        file.write(f'M31 \t\t\t\t; report time \n')                                 # report time
        file.write(f'X = {x_j}, Z = {z_j} \t\t; report position \n')                # current position
        # file.write(f'M114_DETAIL D \t\t\t; report current position \n')           # report position (not working)
        file.write(f'G4 P{wait_time * 1000} \t\t\t; wait time (milliseconds \n')    # Wait specified time

    # file.write(f'G1 X{xz_move[0][0]} Z{origin_z + start_z} F20000\t\t; move to point\n')  # move to point
    file.write(f'G1 Z{1} F20000\t\t\t; return to start Z\n')                            # return to start Z
    file.write(f'G1 X{1} F5000\t\t\t; return to start X\n')                             # return to start X
    file.write('\n\n;end of gcode')                                                     # gcode end line

print(f"file {file_name}.gcode has been created")                                       # print success to terminal

# end of code
