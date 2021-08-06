#/usr/bin/env python
import sys
import os
import binascii
import string
import time
import platform
import Ethenet_sing
import aging_pins
from  ledstatus  import *
from fileModule import *
from  operate_eeprom import *
import multiprocessing
#from oled96x96 import *
from user_led import *


os.chdir("/home/debian/factory-testo-cap3/")


def lock():
        print "lock!"
        while True:
            time.sleep(1)


def init_i2c1():
    os.system("gpio clear 2")
    os.system("gpio clear 3")
    os.system("gpio clear 30")

    

if __name__ == '__main__':
    init_i2c1()
    #Status LED test
    while True:
        status = aging_pins.check_status_led()
        print "-->[01] Status LED Check: done"
        #RGB test
        status = aging_pins.check_rgb()
        print "-->[06] RGB Check: done"
        os.system("gpio set 3")
        #Relay test
        status = aging_pins.check_relay()
        print "-->[07] Relay Check: done"
