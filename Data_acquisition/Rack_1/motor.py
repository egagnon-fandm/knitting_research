'''
Code assumes that motor is connected through a LabJack to the computer. 
'''

# Import libraries
from labjack import ljm
import time
import sys
from enum import Enum

# Motor constants
MAX_POS = 0.16
MIN_POS = 0.020
DIST_PER_TURN = 0.000508
STEPS_PER_TURN = 200

STEP_DIRECTION_OUTPUT = "FIO7" # Step direction output: 0 = up, 1 = down
STEP_OUTPUT = "FIO6" # Step pulses output

dist_per_steps = DIST_PER_TURN/STEPS_PER_TURN

class dir(int, Enum):
    UP = 0
    DOWN = 1

class Motor:

    def __init__(self, initial_pos):
        self.handle = self.connect_to_labjack()
        self.set_clock(self.handle)
        self.config_pulse_output(self.handle)

        self.step_size = 0
        self.total_steps = 0
        self.num_moves = 0
        self.position = initial_pos
        self.step_position = 0
        self.init_position = initial_pos

    def connect_to_labjack(self):
        # Open first found LabJack
        handle = ljm.openS("ANY","ANY","ANY")

        return handle

    def update_travel_settings(self, scan_setting):
        self.step_size = int(scan_setting[2]/dist_per_steps)
        self.total_steps = int(scan_setting[1]/dist_per_steps)
        self.num_moves = int(self.total_steps/self.step_size)
        self.direction = scan_setting[0]

    def check_bounds(self, scan_settings):
        targeted_position = self.init_position

        for scan_setting in scan_settings:
            if scan_setting[0] == dir.UP:
                targeted_position = targeted_position + scan_setting[1]
                
            else:
                targeted_position = targeted_position - scan_setting[1]

        if targeted_position > MAX_POS:
            sys.exit("WARNING: scan moves motor too high.")
        
        if targeted_position < MIN_POS:
            sys.exit("WARNING: scan moves motor too low.")
    

    def set_clock(self, handle):
        # Disable CLOCK0
        result = ljm.eWriteName(handle, "DIO_EF_CLOCK0_ENABLE", 0)
        # Sets clock frequency
        result = ljm.eWriteName(handle, "DIO_EF_CLOCK0_DIVISOR", 8)
        # Sets stepping pulse output rate
        result = ljm.eWriteName(handle, "DIO_EF_CLOCK0_ROLL_VALUE", 30000)
        # Enable CLOCK0
        result = ljm.eWriteName(handle, "DIO_EF_CLOCK0_ENABLE", 1)

    def config_pulse_output(self, handle):
        # Disable extended feature
        result = ljm.eWriteName(handle, "DIO6_EF_ENABLE", 0)
        # Set output to logic low - docs state must start low for proper op
        result = ljm.eWriteName(handle, STEP_OUTPUT, 0)
        # Select the pulse out EF
        result = ljm.eWriteName(handle, "DIO6_EF_INDEX", 2)
        # Number of high-to-low counts
        result = ljm.eWriteName(handle, "DIO6_EF_CONFIG_A", 2000)
        # Number of low-to-high counts
        result = ljm.eWriteName(handle, "DIO6_EF_CONFIG_B", 0)

    def move(self):
        result = ljm.eWriteName(self.handle, STEP_DIRECTION_OUTPUT, self.direction)
        # Number of stepping pulses to generate
        result = ljm.eWriteName(self.handle, "DIO6_EF_CONFIG_C", self.step_size)
        # Enable the pulse out feature and step the motor
        result = ljm.eWriteName(self.handle, "DIO6_EF_ENABLE", 1)
        if self.direction == dir.UP:
            self.step_position = self.step_position+self.step_size
        else:
            self.step_position = self.step_position-self.step_size

        self.position = self.init_position + self.step_position*dist_per_steps

    def move_debug(self, steps, direction):

        result = ljm.eWriteName(self.handle, STEP_DIRECTION_OUTPUT, direction)
        # Number of stepping pulses to generate
        result = ljm.eWriteName(self.handle, "DIO6_EF_CONFIG_C", steps)
        # Enable the pulse out feature and step the motor
        result = ljm.eWriteName(self.handle, "DIO6_EF_ENABLE", 1)

    def wait_on_motion(self):
        # Read number of completed pulses
        num_pulses = ljm.eReadName(self.handle, "DIO6_EF_READ_A")
        # Read number of target pulses
        target_num_pulses = ljm.eReadName(self.handle, "DIO6_EF_READ_B")
    
        # Wait till motion finished
        while num_pulses < target_num_pulses:
            time.sleep(.2)
            # Read number of completed pulses
            num_pulses = ljm.eReadName(self.handle, "DIO6_EF_READ_A")
    
    def scan(self):
        for i in range(self.num_moves):
            self.move_debug(self.step_size,self.direction)
            self.wait_on_motion()

    def read_position(self):
        return self.position
            
    def close(self):
        ljm.close(self.handle)


    def check_next_position(self, dir, step):
        if dir == dir.UP:
            next_pos = self.position + step
            if next_pos >= MAX_POS:
                sys.exit("This exceds the higher bounds.")
        if dir == dir.DOWN:
            next_pos = self.position - step
            if MIN_POS <=next_pos:
                sys.exit("This excedes the lower bounds.")
       