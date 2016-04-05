#############################################################
# Title: Python TCP Client Class                            #
# Description: Wrapper around TCP Client for easy handing   #
#              of TCP communications                        #
# Version:                                                  #
#   * Version 1.0 04/05/2016 RC                             #
#                                                           #
# Author: Richard Cintorino (c) Richard Cintorino 2015      #
#############################################################

import asyncore
import socket
from Debug import pyDebugger

class pyTCPClient(sIP):

    def __init__(self, sIP=127.0.0.1,sPort=8888,sEncryption=False,bDebug = False,sBufferSize=8192):
        self.Debugger = pyDebugger(self,bDebug,False)
        self.IP = sIP
        self.Port = sPort
        self.Encryption = sEncryption
        self.BufferSize = sBufferSize
        self.Connection = None

    def get_interface_ip(self, ifname):
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
            sa.shutdown()
            sa.close()
            self.Debugger.Log("...Set to " + ip,PrintName=False)
        except Exception as e:
            self.Debugger.Log("...FAILED",PrintName=False)
            self.Debugger.Log(str(e))
        return ip

    def Open(self):
        self.Debugger.Log("Attempting to open a connection to " + self.IP + ":" + self.Port + "...",
            endd='')
        try:
            if self.Connection == None:
                self.Connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.Connection.connect((self.IP,self.Port))
                self.Debugger.Log("...Success!",PrintName=False)
                return True
            except Exception as e:
                self.Debugger.Log("...Failed!",PrintName=False)
                self.Debugger.Log(str(e)
                return False

    def Read(self,ReadBytes=None, Blocking=0, AutoConnect=True):
        self.Debugger.Log("Attempting to read data...")
        if ReadBytes == None:
            ReadBytes = self.BufferSize
        if Blocking == 0:
            try:
                sData = self.Connection.recv(ReadBytes)
                self.Debugger.Log("Read: " + sData.decode("UTF-8"))
            except Exception as e:
                self.Debugger.Log("Error")
                self.Debugger.Log(str(e))
        else:
            self.Connection.setblocking(0)
            RtoR = select.select(self.Connection,[],[],Blocking)
            if RtoR[0]:
                try:
                    sData = self.Connection.recv(ReadBytes)
                except Exception as e:
                    self.Debugger.Log("Error")
                    self.Debugger.Log(str(e))
            else:
                sData = ""
        if sData == b'':
            return ""
        else
            return sData.decode("UTF-8")
        
    def Write(self,Data, Blocking=True, AutoConnect=True):
        if Blocking == True:
            bData = Data.encode("UTF-8")
            if len(bData) < self.BufferSize
                self.Connection.send(bData)
            else:
                iChunks = 0
                while iChunks < len(bData):
                    if (iChunks + self.BufferSize) > len(bData):
                        bBufSz = len(bData) - iChunks
                    else:
                        bBufSz = self.BufferSize)
                    self.Connection.send(bData[iChunks:self.BufferSize])
                    iChunks += self.BufferSize
                
    
    
    
    
