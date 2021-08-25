import board
import time
from random import randint
from digitalio import DigitalInOut, Direction, Pull
import busio
import adafruit_framebuf
import adafruit_is31fl3731


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
    display.fill(0, frame=frame)
    display2.fill(0, frame=frame)
    while True:
        display.frame(frame, show=True)
        display2.frame(frame, show=True)

        for _ in range(20):
            x,y,s = randint(0,31), randint(0,7), randint(30,50)

            if x > 15:
                display2.pixel(x%16, y, s, frame)
            else:
                display.pixel(x, y, s, frame)

        for _ in range(20):
            x,y,s = randint(0,31), randint(0,7), randint(0,10)

            if x > 15:
                display2.pixel(x%16, y, s, frame)
            else:
                display.pixel(x, y, s, frame)


def main():
    i2c, sdb, display, display2, buf, fb, frame = initial()
    sorandom(display, display2, frame)

if __name__ == '__main__':
    main()
