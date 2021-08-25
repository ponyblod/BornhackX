import board
import time
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

    # Buttons
    btnA = DigitalInOut(board.BTNA)
    btnA.pull = Pull.UP
    btnB = DigitalInOut(board.BTNB)
    btnB.pull = Pull.UP
    btnX = DigitalInOut(board.BTNX)
    btnX.pull = Pull.UP
    btnY = DigitalInOut(board.BTNY)
    btnY.pull = Pull.UP

    return(i2c, sdb, display, display2, buf, fb, frame, btnX, btnY)

def heart(display, display2, s, btnX, btnY):
    frames = []
    for i in range(8):
        frame = i
        display.frame(frame, show=False)
        display2.frame(frame, show=False)

        coords = [                  (2, 0), (3, 0),         (5, 0), (6, 0), 
                            (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), 
                    (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), 
                    (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), 
                    (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), 
                            (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), 
                                    (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), 
                                            (3, 7), (4, 7), (5, 7), 
                                                    (4, 8)]

        for x, y in coords:
            display.pixel((x+i*2)%16, y, s)
            display2.pixel((x+i*2)%16, y, s)

    direction = 1
    while True:
        if not btnX.value:
            direction = -1
        elif not btnY.value:
            direction = 1

        frame += direction
        display.frame(frame%8, show=True)
        display2.frame(frame%8, show=True)
        time.sleep(0.05)

if __name__ == '__main__':
    i2c, sdb, display, display2, buf, fb, frame, btnX, btnY = initial()
    heart(display, display2, 100, btnX, btnY)
