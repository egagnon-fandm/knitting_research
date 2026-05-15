import numpy as np
import time
import os 
import sys
import motor as mt
import forcegauge as fg
from datetime import datetime
import scan_list_settings as sl

max_force = 2.0 # Maximum force for initial stretch
num_scans = 3 #amount of up and down s
step_size = 0.00025 # distance for one step in m
relaxation_time = 0.5
save_folder_name = "/home/etienne/Documents/Knitted_Fabric/Data"
file_suffix = 'dry3'

# Check if file exists
data_filename = save_folder_name + '/' + 'scan_' + file_suffix + '.dat'
pict_data_filename = save_folder_name + '/' + 'scan_' + file_suffix + '_pict.dat'
if os.path.exists(data_filename) or os.path.exists(pict_data_filename):
    sys.exit('Files already exists')

# Initialize motor and force gauge
motor_initial_pos = 0.0125 #m. NOT USED RIGHT NOW
PORT_NAME = '/dev/ttyUSB0'
motor = mt.Motor(motor_initial_pos)
tb = fg.Torbal(PORT_NAME)

data = np.empty((1,2), dtype='float')
pict_data = np.empty((1,2), dtype='float')

init_pos = motor.read_position()

print(f"Initial position of motor is {init_pos}.")

f = tb.force()

num_steps = 0

pict_index = 0

# Initial move to the max force
print(f"Moving to F = {max_force} in steps of dx = {step_size}.")
while f <= max_force:
    motor.update_travel_settings([mt.dir.DOWN, step_size, step_size])
    motor.move()
    motor.wait_on_motion()

    time.sleep(relaxation_time)

    f = tb.force()

    data = np.append(data, np.array([[motor.read_position(), f]]), axis=0)

    # Count the number of steps
    num_steps = num_steps+1


final_pos = motor.read_position()

# First return to initial position
for i in range(num_steps):
    motor.update_travel_settings([mt.dir.UP, step_size, step_size])
    motor.move()
    motor.wait_on_motion()

    time.sleep(relaxation_time)

    f = tb.force()

    data = np.append(data, np.array([[motor.read_position(), f]]), axis=0)
    print(f"Relaxing scan {1} of {num_scans}. Step {i} of {num_steps}.")

# Remaining scans
for i in range(num_scans-1):
    for j in range(num_steps):
        motor.update_travel_settings([mt.dir.DOWN, step_size, step_size])
        motor.move()
        motor.wait_on_motion()

        time.sleep(relaxation_time)

        f = tb.force()

        data = np.append(data, np.array([[motor.read_position(), f]]), axis=0)
        print(f"Stretching scan {i+2} of {num_scans}. Step {j} of {num_steps}.")

    
    for j in range(num_steps):
        motor.update_travel_settings([mt.dir.UP, step_size, step_size])
        motor.move()
        motor.wait_on_motion()

        time.sleep(relaxation_time)

        f = tb.force()

        data = np.append(data, np.array([[motor.read_position(), f]]), axis=0)
        print(f"Relaxing scan {i+2} of {num_scans}. Step {j} of {num_steps}.")

# Save data
np.savetxt(data_filename, data)
np.savetxt(pict_data_filename, pict_data)

tb.close_port()
motor.close()