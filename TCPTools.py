#############################################################
# Title: Python TCP Tools Class                             #
# Description: Wrapper around TCP Tools for easy handing    #
#              of TCP communications                        #
# Version:                                                  #
#   * Version 1.0 04/07/2016 RC                             #
#                                                           #
# Author: Richard Cintorino (c) Richard Cintorino 2015      #
#############################################################

import asyncore
import socket
import fcntl
import struct
from Debug import pyDebugger

class pyTCPTools():

    def get_interface_ip(self, ifname):
        ip = ""
        try:
            self.Debugger.Log("get_interface_ip: Creating Network Socket...", endd='')
            sa = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.Debugger.Log("Success!",PrintName=False)
        except Exception as e:
            self.Debugger.Log("Failed!",PrintName=False)
            self.Debugger.Log(str(e))
        try:
            self.Debugger.Log("get_interface_ip: Getting IP from interface " + ifname + "...", 
                endd='')
            ip = socket.inet_ntoa(fcntl.ioctl(sa.fileno(), 0x8915, struct.pack('256s', 
                bytes(ifname[:15], 'UTF-8')))[20:24])
            #sa.shutdown(socket.SHUT_RDWR)
            sa.close()
            self.Debugger.Log("...Set to " + ip,PrintName=False)
        except Exception as e:
            self.Debugger.Log("...FAILED",PrintName=False)
            self.Debugger.Log(str(e))
        return ip
