'''
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
from Adafruit_I2C import Adafruit_I2C as I2C 
'''
import mraa
import sys, time, signal
import struct
import os
import subprocess

def check_i2c2():
    status = 'error'
    try:
        out = os.popen("i2cdetect -r -y 2").read()
        if '3c' in out:
            status = 'ok'
    except:
        pass

    return status

def check_rtc():
    status = 'error'
    out = os.popen("hwclock -r -f /dev/rtc0").read()
    print "RTC0 time is: " + str(out)
    time.sleep(1)
    try:
        out = os.popen("hwclock -r -f /dev/rtc1").read()
#        print str(out)
        if 'seconds' in out:
            status = 'ok'
    except:
        pass
    return status,str(out)

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
            if(looptime == 30):
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
            out = os.popen('gpio input 40').read()
            time.sleep(0.2)
            if '0' in out:
                os.system("gpio clear 27")
                return 'ok'
            looptime = looptime + 1
            if(looptime == 40):
                os.system("gpio clear 27")
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
            if(looptime == 10):
                return 'error'
    except:
        pass
    return 'error'

def check_io(): 
    gpio = [112,65,111,31,110,113,14,15]
    gpiopins_out = [112,113,31,14]                                            
    gpiopins_in1 = [65,111,110,15]       
 	    

    pinctl = open("/sys/class/gpio/export", "wb", 0)
    for pin in gpio:
        try:
            pinctl.write( str(pin))
        except:
            print "Pin ", str(pin), " is busy"
    pinctl.close()
    print "export all the GPIO"

    #set output gpio
    for pin in gpiopins_out:
        filename = '/sys/class/gpio/gpio%d/direction' %pin
        try:
            pinctldir = open(filename,"wb",0)
            pinctldir.write("out")
        except:
            print "failed to set direction of pin %d" %pin
            pinctldir.close()
    #set input group1
    for pin in gpiopins_in1:
        filename = '/sys/class/gpio/gpio%d/direction' %pin
        try:
            pinctldir = open(filename,"wb",0)
            pinctldir.write("in")
        except:
            print "failed to set direction of pin %d" %pin
            pinctldir.close()

    os.system("echo 0 > /sys/class/gpio/gpio%d/value" %gpiopins_out[0])  
    os.system("echo 0 > /sys/class/gpio/gpio%d/value" %gpiopins_out[1])	
    os.system("echo 0 > /sys/class/gpio/gpio%d/value" %gpiopins_out[2])	
    os.system("echo 0 > /sys/class/gpio/gpio%d/value" %gpiopins_out[3])	
    time.sleep(0.1)
    badio1 = []
    value = []
    for pin in gpiopins_in1:
        values = os.popen("cat /sys/class/gpio/gpio%d/value" %pin).read().strip()
        value.append(values)
        if values != "0":
            badio1.append(pin)
    print value
    
    time.sleep(0.1)
	
    os.system("echo 1 > /sys/class/gpio/gpio%d/value" %gpiopins_out[0])  
    os.system("echo 1 > /sys/class/gpio/gpio%d/value" %gpiopins_out[1])		
    os.system("echo 1 > /sys/class/gpio/gpio%d/value" %gpiopins_out[2])  
    os.system("echo 1 > /sys/class/gpio/gpio%d/value" %gpiopins_out[3])  
    time.sleep(0.01)	
    badio2 = []
    value = []
    for pin in gpiopins_in1:
        values = os.popen("cat /sys/class/gpio/gpio%d/value" %pin).read().strip() 
        value.append(values)
        if values != "1":
            badio2.append(pin)
    print value

    badio = badio1 + badio2             
    return badio
    
def check_voltage():
    ain0 = mraa.Aio(0)
    ain4 = mraa.Aio(4)
    ain5 = mraa.Aio(5)

    times = 100
    sum = 0
    values = []
     
    
    VOLTAGES = [["AIN0", 1.45, 1.85, ain0],
                ["AIN4", 1.54, 1.78, ain4],
                ["AIN5", 1.54, 1.78, ain5],
               ] 
                
    # ADC.setup()
    result = []
    status = 'ok'
    for v in VOLTAGES:
        ain = v[3].read()/1024.0*1.8    #ain = ADC.read(v[0])*1.8        
        #print ain
        if ain < v[1] or ain > v[2]:
            result.append('%f (%s) is out of range: %f ~ %f.' % (ain, v[0], v[1], v[2]))
            status = 'error'
        else:
            result.append('%f (%s) is in of range: %f ~ %f.' % (ain, v[0], v[1], v[2]))    
    return  status,result

def check_battery():
    isok = 'error'
    battery_status = int(subprocess.check_output(['i2cget', '-y' ,'-f', '0', '0x24', '0x3']).strip(), 16)
    if (battery_status == 0x48) or (battery_status ==0x08) or (battery_status ==16):
        isok = 'ok'
    return isok,battery_status
    
if __name__ == '__main__':
#    print "i2c bus check: " + check_i2c2()
    status,result = check_rtc()
    print status
    print result
#    print check_io() 
#    print "status led check: " + check_status_led()   
#    time.sleep(2)
#    print "RGB LED check: " + check_rgb()
#    time.sleep(2)
#    print "relay check: " + check_relay()
#    print check_voltage()
#    print check_battery()
