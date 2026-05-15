import numpy as np
import time
import motor as mt

# BEWARE. Boundry checks are disabled and moving the motor too far could result in damage.
step_size = 0.005 # Size in meters 1 = 1 m, 0.1 = 10 cm, 0.01 = 1 cm, 0.001  = 1mm
step_dir = mt.dir.DOWN
if __name__ == "__main__":
    motor = mt.Motor(0.0)
    motor.update_travel_settings([step_dir, step_size, step_size])

    motor.move()
    motor.wait_on_motion()

    motor.close()