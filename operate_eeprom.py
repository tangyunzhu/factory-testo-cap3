import os
import sys
import struct
import time
'''
struct am335x_baseboard_id {
       u8 magic[4];
       u8 name[8];
       u8 version[4];
       u8 serial[12];
       u8 config[32];
       u8 mac_addr[3][6];
};
#define as I8sI12s32s18s
'''
eeprom_path = "/sys/devices/platform/ocp/4802a000.i2c/i2c-1/1-0050/eeprom"
class eeprom:
    def __init__(self,dumpName = ''):
        self.eeprom_dump = struct.Struct("I8s4s12s32s18s")
        self.eeprom_path = "/sys/devices/platform/ocp/4802a000.i2c/i2c-1/1-0050/eeprom"

    def readBoardinfo(self):
        self.fp_sys = open(eeprom_path,'rb')
        self.eeprom_dump = self.fp_sys.read(78)

        self.magic,\
        self.name,\
        self.version,\
        self.serial,\
        self.config,\
        self.mac_addr = \
            struct.unpack("I8s4s12s32s18s",self.eeprom_dump)

        self.fp_sys.close()
        print self.name,self.version,self.serial,self.config,self.mac_addr
        return self.name,self.version,self.serial,self.config


    def writeBoardinfo(self,new_name,new_version,new_serial,new_config):
        self.fp_local = open('eeprom.dump','wb+')
        self.name = new_name
        self.version = new_version
        self.serial = new_serial
        self.config = new_config
        print "Read from eeprom.dump"
        print self.name
        print self.version
        print self.serial
        print self.config
        self.eeprom_dump = struct.pack('I8s4s12s32s18s', self.magic,\
                                                        self.name,\
                                                        self.version,\
                                                        self.serial,\
                                                        self.config,\
                                                        self.mac_addr)
        self.fp_local.write(self.eeprom_dump)
        self.fp_local.close()
        os.system("sync")
        os.popen('hexdump -C ./eeprom.dump').read()

    	os.system("dd if=./eeprom.dump of=" + self.eeprom_path)
        os.system("sync")

    def dd_name_2_eeprom(self):
        os.system("dd if=/root/factory_test/eeprom_bk.dump of=" + self.eeprom_path + " bs=1k")

#Test eeprom class
if __name__ == '__main__':
    Myeeprom = eeprom()
    Myeeprom.dd_name_2_eeprom()
        
	# read
    name,version,serial,config = Myeeprom.readBoardinfo()
    print "Read from eeprom"
    print name
    print version
    print serial
    print config
	# write
    utc_time = time.time()
    time_list = str(utc_time).split(".")
    version = 'TGB1'
    name = '04602803'
#    serial = 'BBG115050016'
    serial_id =os.popen("cat test_id.txt").read().strip() 
    serial = "TGB" + serial_id
    config = time_list[0]
    Myeeprom.writeBoardinfo(name,version,serial,config)

    name,version,serial,config = Myeeprom.readBoardinfo()
    print "Read from eeprom final"
    print name
    print version
    print serial
    print config
    new_serial_id = int(serial_id) + 1
    cmd = "echo {} > test_id.txt".format(new_serial_id)
    os.popen(cmd)
