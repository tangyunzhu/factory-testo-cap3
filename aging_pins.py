'''
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
from Adafruit_I2C import Adafruit_I2C as I2C 
'''
import sys, time, signal
import struct
import os
import subprocess

def check_status_led():
    status = 'error'
    looptime = 0
    try:
        out = os.popen('gpio input 40').read()
        if '0' in out:
            return 'error'
        looptime = 0
        while True:
            os.system('gpio set 22')
            time.sleep(0.2)
            os.popen('gpio clear 22')
            time.sleep(0.2)
            out = os.popen('gpio input 40').read()
            if '0' in out:
                return 'ok'
            looptime = looptime + 1
            if(looptime == 5):
                return 'error'
    except:
        pass
    return 'error'

def check_relay():
    status = 'error'
    looptime = 0
    try:
        os.system('gpio set 27')
        while True:
            os.system('gpio set 27')
	    time.sleep(1)
	    os.system('gpio clear 27')
	    time.sleep(1)
            looptime = looptime + 1
            if(looptime == 5):
                return 'error'
    except:
        pass
    os.system("gpio clear 27")
    return 'error'

def check_rgb():
    status = 'error'
    try:
        out = os.popen('gpio input 40').read()
        if '0' in out:
            return 'error'
        looptime = 0
        while True:
            os.system('gpio set 2')
            time.sleep(0.2)
            os.popen('gpio clear 2')
            os.popen('gpio set 3')
            time.sleep(0.2)
            os.popen('gpio clear 3')
            os.popen('gpio set 30')
            time.sleep(0.2)
            os.popen('gpio clear 30')
            time.sleep(0.2)
            out = os.popen('gpio input 40').read()
            if '0' in out:
                return 'ok'
            looptime = looptime + 1
            if(looptime == 5):
                return 'error'
    except:
        pass
    return 'error'

def check_battery():
    isok = 'error'
    battery_status = int(subprocess.check_output(['i2cget', '-y' ,'-f', '0', '0x24', '0x3']).strip(), 16)
    if (battery_status == 0x48) or (battery_status ==0x08) or (battery_status ==16):
        isok = 'ok'
    return isok,battery_status
    
if __name__ == '__main__':
#    print "i2c bus check: " + check_i2c2()
#    status,result = check_rtc()
#    print status
#    print result
#    print check_io() 
#    print "status led check: " + check_status_led()   
#    time.sleep(2)
    print "RGB LED check: " + check_rgb()
#    time.sleep(2)
#    print "relay check: " + check_relay()
#    print check_voltage()
#    print check_battery()
