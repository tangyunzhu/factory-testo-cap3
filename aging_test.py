#/usr/bin/env python
import sys
import os
import binascii
import string
import time
import platform
import Ethenet_sing
import pins
from  ledstatus  import *
from fileModule import *
from  operate_eeprom import *
import multiprocessing
from oled96x96 import *
from user_led import *


os.chdir("/root/factory_test/")


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
    status = pins.check_status_led()
    print "-->[01] Status LED Check: " + str(status)
      

    #RGB test
    status = pins.check_rgb()
    print "-->[06] RGB Check: " + str(status)
        
    while True:
        out = os.popen('gpio input 40').read()
        if '1' in out:
            break
    os.system("gpio set 3")
    #Relay test
    status = pins.check_relay()
    print "-->[07] Relay Check: " + str(status)
            
