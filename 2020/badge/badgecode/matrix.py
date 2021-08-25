import board
import time
from digitalio import DigitalInOut, Direction, Pull
import busio
import adafruit_framebuf
import adafruit_is31fl3731
from random import randint


def initial():
    # configure I2C
    i2c = busio.I2C(board.SCL, board.SDA)

    # turn on LED drivers
    sdb = DigitalInOut(board.SDB)
    sdb.direction = Direction.OUTPUT
    sdb.value = True

    # set up the two LED drivers
    display = adafruit_is31fl3731.Matrix(i2c, address=0x74)
    display2 = adafruit_is31fl3731.Matrix(i2c, address=0x77)

    # Create a framebuffer for our display
    buf = bytearray(64)  # 2 bytes tall x 32 wide = 64 bytes (9 bits is 2 bytes)
    fb = adafruit_framebuf.FrameBuffer(
        buf, display.width*2, display.height, adafruit_framebuf.MVLSB
    )

    frame = 0  # start with frame 0

    return(i2c, sdb, display, display2, buf, fb, frame)

def sorandom(display, display2, frame):
    # sorandom(display, display2, frame)
    while True:
        display.fill(0, frame=frame)
        display2.fill(0, frame=frame)
        display.frame(frame, show=True)
        display2.frame(frame, show=True)

        for _ in range(200):
            x,y,s = random.randint(0,31), random.randint(0,7), random.randint(0,30)

            if x > 15:
                display2.pixel(x%16, y, s, frame)
            else:
                display.pixel(x, y, s, frame)
            time.sleep(0.1)

        frame = 0 if frame else 1


def matrix(display, display2):
    pass

def main():
    i2c, sdb, display, display2, buf, fb, frame = initial()
    matrix(display, display2)

if __name__ == '__main__':
    main()
