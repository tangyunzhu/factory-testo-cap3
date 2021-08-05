#/usr/bin/env python
import sys
import os
import binascii
import string
import time
import barcode
import  serial
import platform
import Ethenet_sing
import pins
from  ledstatus  import *
from fileModule import *
from  operate_eeprom import *
import multiprocessing
from oled96x96 import *
from user_led import *
from alicloud_upload import *

os.chdir("/root/factory_test/")
uploader = log_uploader()
UploadFileName = ""
oled = OLED96x96()

def lock():
        print "lock!"
        while True:
            time.sleep(1)
def report_error():
    print"Test Error"
    for n in range(0,100):
        print "uploading log file"
        f = uploader.uploadfile(UploadFileName[26:],UploadFileName)
        if f == True:
            break
      
    os.system("sync")
    os.system("gpio clear 3")
    os.system("gpio set 2")
    while True:
        out = os.popen('gpio input 40').read()
        if '0' in out:
            break
    os.system("poweroff")

def init_i2c1():
    os.system("gpio clear 2")
    os.system("gpio clear 3")
    os.system("gpio clear 30")
    os.system("config-pin P9_17 i2c")
    os.system("config-pin P9_18 i2c")
    time.sleep(1)
    os.system("echo rx8025 0x32 > /sys/devices/platform/ocp/4802a000.i2c/i2c-1/new_device")
    os.system("echo 24c32 0x50 > /sys/devices/platform/ocp/4802a000.i2c/i2c-1/new_device")
    time.sleep(1)
    os.system("hwclock -w -f /dev/rtc1")
    time.sleep(2)
    os.system("hwclock -w -f /dev/rtc1")
    time.sleep(1)


    

if __name__ == '__main__':
    init_i2c1()
    try:
        global UploadFileName
        oled.myPrint("Barcode", "RD")
        id = barcode.readID()
        eeprom_serial = "TGB1" + id[11:]
        report_file = id
        okfile = id
        print  report_file

        if report_file != 'blank':
            report_file = "/root/factory_test/report/"+report_file+ '_' + str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time())))+'_fail'+".txt"
            okfile = "/root/factory_test/report/"+okfile + '_' + str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time())))+'_pass'+".txt"
#            print "report_file is: " + report_file
#            print "okfile is: " + okfile
            UploadFileName = report_file
            report = open(report_file,'w+')
            print "report_file: " + report_file
        else:
            report_error()
        report.write("That's TestoReader Seiral:" + report_file + " production test report!\n")
        report.write("if you have any questions about this test reports,Please conntact:www.seeedstudio.com\n")
        report.write("Software System:" + platform.linux_distribution()[0] + ' ' + platform.linux_distribution()[1] + '\n')

        report.write("Hardware test:\n")
        report.write("************************************************************************\n")
        report.close()

        #Status LED test
        os.system("echo \"" + "----------------------------Status LED test---------------------------\n" + "\" >> " + report_file)
        oled.myPrint("LED", "       ")
        status = pins.check_status_led()
        print "-->[01] Status LED Check: " + str(status)
        oled.printBackLine()
        if status == 'ok':
            oled.myPrint("LED", "   OK  ")
            os.system("echo \"" + "Status LED test----->[pass]\n\n" + "\" >> " + report_file)
        else:
            oled.myPrint("LED", "   Fail")
            os.system("echo \"" + "Status LED test----->[fail]\n\n" + "\" >> " + report_file)
            report_error()   
            
        #Battery test
        os.system("echo \"" + "----------------------------Battery test---------------------------\n" + "\" >> " + report_file)
        oled.myPrint("BAT", "       ")
        status,result = pins.check_battery()
        print "-->[02] Battery return value is:[0x08,0x48] " + str(status)
        os.system("echo \""  + "PMU return value is[expect: 0x08 or 0x48]: "+ str(result) + "\n\" >> " + report_file)
        oled.printBackLine()
        if status == 'ok':
            oled.myPrint("BAT", "   OK  ")
            os.system("echo \"" + "Battery test----->[pass]\n\n" + "\" >> " + report_file)
        else:
            oled.myPrint("BAT", "   Fail")
            os.system("echo \"" + "Battery test----->[fail]\n\n" + "\" >> " + report_file)
            report_error()			

        # GPIO test
        os.system("echo \"" + "------------------------------ GPIO test------------------------------\n" + "\" >> " + report_file)
        print "-->[03] GPIO check"
        badio = []
        oled.myPrint("GPIO", "      ")
        badio = pins.check_io()
        oled.printBackLine()
        if len(badio) != 0:
            oled.myPrint("GPIO", "  Fail")
            os.system("echo \"" + "gpio test ------>[fail]\n\n" + "\" >> " + report_file)
            for pin in badio:
                #report.write(str(pin) +'\n')
                os.system("echo \"" + str(pin) + "\n" + "\" >> " + report_file)
            report_error()
        else:
            oled.myPrint("GPIO", "  OK  ")
            os.system("echo \"" + "gpio test ------>[pass]\n\n" + "\" >> " + report_file)

        # analog pins test
        os.system("echo \"" + "----------------------------analog pins test---------------------------\n" + "\" >> " + report_file)
        oled.myPrint("ANALOG", "    ")
        status,result = pins.check_voltage()
        print "-->[04] Analog pin check  " + status
        for v in result:
            os.system("echo \""+ v + "\n\" >> " + report_file)
        oled.printBackLine()
        if status == 'ok':
            oled.myPrint("ANALOG", "OK  ")
            os.system("echo \"" + "analog pins test   ------>[pass]\n\n" + "\" >> " + report_file)
        else:
            oled.myPrint("ANALOG", "Fail")
            os.system("echo \"" + "analog pins test   ------>[fail]\n\n" + "\" >> " + report_file)
            report_error()

        #RTC test
        os.system("echo \"" + "----------------------------RTC test---------------------------\n" + "\" >> " + report_file)
        oled.myPrint("RTC", "       ")
        status,result1 = pins.check_rtc()
        print "-->[05] RTC1 Read status: " + str(status)
        print "-->[05] RTC1 Read result: " + str(result1)
        os.system("echo \""  + "hwclock read RTC1\n\ "+ str(result1) + "\n\" >> " + report_file)
        oled.printBackLine()
        if status == 'ok':
            oled.myPrint("RTC", "   OK  ")
            os.system("echo \"" + "RTC test----->[pass]\n\n" + "\" >> " + report_file)
        else:
            oled.myPrint("RTC", "   Fail")
            os.system("echo \"" + "RTC test----->[fail]\n\n" + "\" >> " + report_file)
            report_error()
        

        #RGB test
        os.system("echo \"" + "----------------------------RGB LED test---------------------------\n" + "\" >> " + report_file)
        oled.myPrint("RGB", "       ")
        status = pins.check_rgb()
        print "-->[06] RGB Check: " + str(status)
        oled.printBackLine()
        if status == 'ok':
            oled.myPrint("RGB", "   OK  ")
            os.system("echo \"" + "RGB LED test----->[pass]\n\n" + "\" >> " + report_file)
        else:
            oled.myPrint("RGB", "   Fail")
            os.system("echo \"" + "RGB LED test----->[fail]\n\n" + "\" >> " + report_file)
            report_error()  
        
        while True:
            out = os.popen('gpio input 40').read()
            if '1' in out:
                break
        os.system("gpio set 3")
        #Relay test
        os.system("echo \"" + "----------------------------Relay test---------------------------\n" + "\" >> " + report_file)
        oled.myPrint("RLY", "       ")
        status = pins.check_relay()
        print "-->[07] Relay Check: " + str(status)
        oled.printBackLine()
        if status == 'ok':
            oled.myPrint("RLY", "   OK  ")
            os.system("echo \"" + "Relay test----->[pass]\n\n" + "\" >> " + report_file)
        else:
            oled.myPrint("RLY", "   Fail")
            os.system("echo \"" + "Relay test----->[fail]\n\n" + "\" >> " + report_file)
            report_error()             
            
            
        '''eeprom test'''
        os.system("echo \"" + "------------------------------eeprom test-------------------------------\n" + "\" >> " + report_file)
        oled.myPrint("EEPROM", "  ")
        Myeeprom = eeprom()
        Myeeprom.dd_name_2_eeprom()
        name,version,serial,config = Myeeprom.readBoardinfo()
        print "default name is: " + name
        print "default version is: " + version
        print "default serial is: " + serial
                
        name = '04602803'
        version = 'TGB1'
        serial = eeprom_serial
        utc_time = time.time()
        time_list = str(utc_time).split(".")
        config = time_list[0]
        Myeeprom.writeBoardinfo(name,version,serial,config)
        name,version,serial,config = Myeeprom.readBoardinfo()
        oled.printBackLine()
        if serial == eeprom_serial:
            oled.myPrint("EEPROM", "OK")
            cmd1 = "echo \"write board serial:  {} ------>[PASS]\n\" >> ".format(serial) + report_file
            cmd2 = "echo \"write board version: {} ------>[PASS]\n\" >> ".format(version) + report_file
            os.system(cmd1)
            os.system(cmd2)
        else:
            oled.myPrint("EEPROM", "Fail")
            cmd1 = "echo \"write board serial:  {} ------>[FAIL]\n\" >> ".format(serial) + report_file
            cmd2 = "echo \"write board version: {} ------>[FAIL]\n\" >> ".format(version) + report_file
            os.system(cmd1)
           
        cmd = "hexdump -C -v -n 128 -s 0 " + "/sys/devices/platform/ocp/4802a000.i2c/i2c-1/1-0050/eeprom >> " + report_file
        os.system(cmd)         
        os.system("mv "+report_file+" "+okfile)
        os.system("sync")
        os.system("sync")
        UploadFileName = okfile
        for n in range(0,100):
            print "uploading log file"
            f = uploader.uploadfile(UploadFileName[26:],UploadFileName)
            if f == True:
                break   
        os.system("gpio clear 3")     
        os.system("poweroff")

    except Exception as e:
        print e
        os.system("echo \"" + str(e) + "\" > log.out" )
        report_error()
