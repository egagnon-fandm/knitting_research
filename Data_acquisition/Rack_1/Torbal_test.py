import time
import forcegauge as fg
#from pynput.keyboard import Key, Listener

# Force gauge constants
PORT_NAME = '/dev/ttyUSB0'

tb = fg.Torbal(PORT_NAME)
i = 0
while True:
    time.sleep(.1)
    print("Iter: {:}, Force: {:.3f} {:}\n".format(i, tb.force(), tb.units))
    i = i + 1
tb.close_port()



# def on_press(key):
#     print('{0} pressed'.format(
#         key))

# def on_release(key):
#     print('{0} release'.format(
#         key))
#     if key == Key.esc:
#         # Stop listener
#         return False

# # Collect events until released
# with Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()