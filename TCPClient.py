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

class pyTCPClient():

    def __init__(self, sIP="127.0.0.1",sPort=8888,sEncryption=False,bDebug = False,sBufferSize=8192):
        self.RetryAttempts = 10
        self.Debugger = pyDebugger(self,bDebug,False)
        self.IP = sIP
        self.Port = int(sPort)
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
        self.Debugger.Log("Attempting to open a connection to " + self.IP + ":" + str(self.Port) +
            "...", endd='')
        if self.Connection == None:
            self.Connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.Connection.connect((self.IP,self.Port))
            self.Debugger.Log("...Success!",PrintName=False)
            return True
        except Exception as e:
            self.Debugger.Log("...Failed!",PrintName=False)
            self.Debugger.Log(str(e))
            return False
     

    def Read(self,ReadBytes=None, Blocking=0, AutoConnect=True):
        self.Debugger.Log("Attempting to read data from " + self.IP + ":" + str(self.Port) + "...")
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
        else:
            return sData.decode("UTF-8")
        
    def Write(self,Data, Blocking=True, AutoConnect=True,pParent=None):
        if Blocking == True:
            return self._write(Data,AutoConnect,None)
        else:
            threading.Thread(target=self._write, args=(self,Data,AutoConnect,pParent)).start()
        
    def _write(self,Data, AutoConnect,pParent):
        self.Debugger.Log("Attempting to write data to " + self.IP + ":" + str(self.Port) + "...")
        iChunks = 0
        numTries = 0
        bData = Data.encode("utf-8")
        while iChunks < len(bData):
            numTries += 1
            if (iChunks + self.BufferSize) > len(bData):
                bBufSz = len(bData) - iChunks
            else:
                bBufSz = self.BufferSize
            try:
                self.Debugger.Log("Writing " + str(bBufSz) + " bytes...",endd='')
                if self.Connection == None and AutoConnect == True:
                    #self.Debugger.Log("Automatically opening connection to " + self.IP + ":" + 
                        #self.Port + "...",endd='')
                    self.Open()
                    #if self.Open() == True:
                        #self.Debugger.Log("...Success!",PrintName=False)
                    #else:
                        #self.Debugger.Log("...Failed!",PrintName=False)
                        #return 0
                self.Connection.send(bData[iChunks:(iChunks+bBufSz)])
                self.Debugger.Log("...Success! (" + str(numTries) + " attempts)",PrintName=False)
                iChunks += bBufSz
                numTries = 0
            except Exception as e:
                self.Debugger.Log("...Failed (" + str(numTries) + " attempts)",PrintName=False)
                self.Debugger.Log("Closing Connection...")
                self.Connection = None
                self.Debugger.Log(str(e))
                if numTries >= self.RetryAttempts:
                    break;    
        if pParent == None:
            return iChunks
        else:
            pParent.WriteCallBack(iChunks)
            
    
    
    
    
