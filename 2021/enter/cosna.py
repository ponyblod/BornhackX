# -*- coding: utf-8 -*-
import bluetooth
import binascii
import codecs


class Cosna(object):
    def __init__(self, mac_address, verbose=False):
        self.mac_address = mac_address
        self.sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.verbose = verbose

    # bytes:
    # 1 length: 0x0a
    # 2 random: r
    # 3 c_-94 xor r
    # 4 source xor r (8 for picker, 18 for something else?)
    # 5 red xor r
    # 6 green xor r
    # 7 blue xor r
    # 8 0 xor r
    # 9 0 xor r
    # 10 checksum: 0- (length+r+b3+b4+b6+b7+b8+b9+b10)
    def generate_hexstring(self, r, g, b, random=0xff, source=8):
        length, rc94, rsource = 0x0a, (256 - 94) ^ random, source ^ random
        rred, rgreen, rblue = r ^ random, g ^ random, b ^ random
        rzero = 0 ^ random
        checksum = (length + random + rc94 + rsource + rred + rgreen + rblue + rzero + rzero) % 256
        return bytearray([length, random, rc94, rsource, rred,
                          rgreen, rblue, rzero, rzero, 256 - checksum])

    def connect(self):
        # print "connecting and sending switch commands"
        if self.verbose: print(('connecting to %s') % self.mac_address)
        self.sockfd.connect((self.mac_address, 1))  # BT Address
        if self.verbose: print('connected')

    def disconnect(self):
        if self.verbose: print('disconnecting')
        self.sockfd.close()

    def change_color(self, r, g, b):
        hex = self.generate_hexstring(r, g, b)
        hex = codecs.decode(binascii.hexlify(hex).decode('utf-8'), 'hex')  
        self.sockfd.send((hex))
        self.sockfd.send('\r')

        # sockfd.send(chr(26))  # CTRL+Z
        # sockfd.close()
