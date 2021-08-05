import os
import sys


def get_mac_addr():
    mac_addr = {'eth0':'00:11:22:33:44:55','eth1':'00:11:22:33:44:56'}
    for line in os.popen("/sbin/ifconfig"):
        if line[0:4] == 'eth0':
            x = {'eth0':line[-20:][0:17]}
            mac_addr.update(x)
        if line[0:4] == 'eth1':
            x = {'eth1':line[-20:][0:17]}
            mac_addr.update(x)
    return  mac_addr

def do_shell_command(cmd):
    error = 'error'
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        return output
    else:
        error = 'ok'
        return  error

def get_ip_address():
    lines = os.popen("ifconfig eth0").read()
    start_num = lines.find("inet addr:")
    stop_num = lines.find("Bcast:")
    line = lines[start_num+10:stop_num]
    line = line.replace(" ","")
    list_ip = line.split(".")
    ip_address = list_ip[0] + "."+ list_ip[1] + "." + list_ip[2] + "." + list_ip[3]
    return ip_address

def do_ethernet_dhcp():
    ip_address = get_ip_address()
    if "192.168." not in ip_address:
        print "ip address error"
        return 'error',ip_address
    print "ip address is: " + ip_address
    ip_address1 = ip_address + ".1"
    ip_address2 = ip_address + ".2"

    cmd3 = "ping -l 16 -c 1 www.baidu.com"
    result = 'error'

    for line in os.popen(cmd3):
        print line
        if "1 received, 0% packet loss" in line:
            result = 'ok'
            return result,ip_address
    return result,ip_address
if __name__ == '__main__':
    flag,ip = do_ethernet_dhcp()
    if flag == 'ok':
        print "ethernet test ok!"
    else:
        print "ethernet test fail!"

