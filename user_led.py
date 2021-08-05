import os
import time

def rgb_led_init():
    os.system("echo 110 > /sys/class/gpio/export")
    os.system("echo 51 > /sys/class/gpio/export")
    os.system("echo 50 > /sys/class/gpio/export")
    os.system("echo out > /sys/class/gpio/gpio110/direction")
    os.system("echo out > /sys/class/gpio/gpio51/direction")
    os.system("echo out > /sys/class/gpio/gpio50/direction")
    
def rgb_led_white():
    os.system("gpio clear 50")
    os.system("gpio set 115")
    time.sleep(0.4)
    os.system("gpio clear 115")
    os.system("gpio set 51")
    time.sleep(0.4)
    os.system("gpio clear 51")
    os.system("gpio set 50")
    time.sleep(0.4)

def rgb_led_off():
    os.system("echo 0 > /sys/class/gpio/gpio51/value")
    os.system("echo 0 > /sys/class/gpio/gpio50/value")
    os.system("echo 0 > /sys/class/gpio/gpio110/value")
    
def userLed1On():
	os.system('echo 255 > /sys/class/leds/beaglebone:green:usr0/brightness')

def userLed1Off():
	os.system('echo 0 > /sys/class/leds/beaglebone:green:usr0/brightness')

def userLed2On():
	os.system('echo 255 > /sys/class/leds/beaglebone:green:usr1/brightness')

def userLed2Off():
	os.system('echo 0 > /sys/class/leds/beaglebone:green:usr1/brightness')

def userLed3On():
	os.system('echo 255 > /sys/class/leds/beaglebone:green:usr2/brightness')

def userLed3Off():
	os.system('echo 0 > /sys/class/leds/beaglebone:green:usr2/brightness')
	
def userLed4On():
	os.system('echo 255 > /sys/class/leds/beaglebone:green:usr3/brightness')
	
def userLed4Off():
	os.system('echo 0 > /sys/class/leds/beaglebone:green:usr3/brightness')
    
def userLedAllOn():
	userLed1On()
	userLed2On()
	userLed3On()
	userLed4On()

def userLedAllOff():
	userLed1Off()
	userLed2Off()
	userLed3Off()
	userLed4Off()

    
if __name__ == '__main__':
    rgb_led_init()
    while True:
        rgb_led_white()
