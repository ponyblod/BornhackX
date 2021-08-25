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

    return(i2c, sdb, display, display2, buf, fb, frame, btnA, btnB, btnY, btnX)


def heart(display, display2, s):
    # heart(display, display2, 30)
    for i in range(8):
        frame = i
        display.frame(frame, show=False)
        display2.frame(frame, show=False)

        coords = [(2, 0), (3, 0), (5, 0), (6, 0), 
                (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), 
                (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), 
                (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), 
                (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), 
                (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), 
                (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), 
                (3, 7), (4, 7), (5, 7), 
                (4, 8)]

        for x,y in coords:
            display.pixel((x+i*2)%16, y, s)
            display2.pixel((x+i*2)%16, y, s)

    while True:
        for frame in range(8):
            display.frame(frame, show=True)
            display2.frame(frame, show=True)
            time.sleep(0.1)


def etch_N_sketch(btnA, btnB, btnY, btnX, display, display2, frame):
    # etch_N_sketch(btnA, btnB, btnY, btnX, display, display2, frame)
    x, y, s = 0, 0, 30
    display.frame(frame, show=True)
    display2.frame(frame, show=True)
    display.pixel(0, 0, s, frame)


    while True:
        if btnA.value and btnB.value and btnY.value and btnX.value:
            continue
            
        if not btnA.value and not btnB.value:
            display.fill(0, frame)
            display2.fill(0, frame)
            x, y = 0, 0
            while not btnA.value and not btnB.value:
                time.sleep(1)

        elif not btnA.value:
            y-=1
        elif not btnB.value:
            y+=1
        elif not btnY.value:
            x+=1
        elif not btnX.value:
            x-=1

        if x%32 > 15:
            display2.pixel(x%16, y%9, s, frame)
        else:   
            display.pixel(x%16, y%9, s, frame)

        time.sleep(0.05)

def etch_N_erase(btnA, btnB, btnY, btnX, display, display2, frame):
    x, y, s = 0, 0, 30
    ledbuf = [[x,y]]
    display.frame(frame, show=True)
    display2.frame(frame, show=True)
    display.pixel(x, y, s, frame)

    while True:
        if btnA.value and btnB.value and btnY.value and btnX.value:
            continue

            
        if not btnA.value and not btnB.value:
            display.fill(0, frame)
            display2.fill(0, frame)
            x, y = 0, 0
            while not btnA.value and not btnB.value:
                time.sleep(1)

        elif not btnA.value:
            y-=1
        elif not btnB.value:
            y+=1
        elif not btnY.value:
            x+=1
        elif not btnX.value:
            x-=1

        if x%32 > 15:
            display2.pixel(x%16, y%9, s, frame)
        else:   
            display.pixel(x%16, y%9, s, frame)

        time.sleep(0.05)

        currled = [x%32,y%18]
        if currled in ledbuf:
            ledbuf.remove(currled)
            if x%32 > 15:
                display2.pixel(x%16, y%9, 0, frame)
            else:
                display.pixel(x%16, y%9, 0, frame)
            continue

        ledbuf.append(currled)


def main():
    i2c, sdb, display, display2, buf, fb, frame, btnA, btnB, btnY, btnX = initial()
    etch_N_sketch(btnA, btnB, btnY, btnX, display, display2, frame)

if __name__ == '__main__':
    main()
