from cosna import Cosna
from evdev import InputDevice, categorize, ecodes
from time import sleep
from random import choice
from itertools import product

# bt_remote_addr = "00:E0:4C:XX:XX:XX"
# replace the mac address to be the one for your the device
mac_address = "00:E0:4C:8A:80:0A"
cos = Cosna(mac_address, True)
device = InputDevice('/dev/input/event0')
values = [0,99]

colors = [x for x in product(values, repeat=3)]
colors.remove((0,0,0))
colors.remove((99,99,99))

# Connect to device
cos.connect()

# Change color three times, with 2 seconds between
print('Running')
try:
    while True:
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)

                if key_event.keystate == 1: # 0 == Up, 1 == Down, 2 == Hold
                    r, g, b = choice(colors) 
                    print(f'Down: {r} {g} {b}')
                    cos.change_color(r,g,b)


finally:
    cos.change_color(0,0,0)
    # Disconnecting
    cos.disconnect()
    print('Test is done!')
