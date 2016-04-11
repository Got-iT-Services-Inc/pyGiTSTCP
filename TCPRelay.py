#############################################################
# Title: Python TCP Server Class                            #
# Description: Wrapper around TCP Server for easy handing   #
#              of TCP communications                        #
# Version:                                                  #
#   * Version 1.0 10/22/2015 RC                             #
#   * Version 2.0 04/05/2016 RC - Update names              #
#                                                           #
# Author: Richard Cintorino (c) Richard Cintorino 2015      #
#############################################################

import asyncore
import socket
from Debug import pyDebugger

class TCPSHandler(asyncore.dispatcher_with_send):

    #Server Variables
    IP = "192.168.1.103"
    Port = 10000
    BufferSize = 8192

    def __init__:
        self.Debugger = pyDebugger(self,True,False)

    def handle_read(self):
        data = self.recv(self.BufferSize)
        if data:
            self.Debugger.Log("Received Data: " + data.decode('UTF-8'))
            self.Debugger.Log("Opening connection to Relay at " + self.IP + ":" + str(self.Port) + "...", endd="")
            try:
                Relay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                Relay.connect((self.IP,self.Port))
                self.Debugger.Log("Success!",PrintName=False)
            except:
                self.Debugger.Log("Failed!",PrintName=False)
                self.Debugger.Log("***Error: Could not connect to Relay!****")

            try:
                self.Debugger.Log("Transmitting data to Relay...", endd='')
                Relay.sendall(bytes(data.decode('UTF-8') + "\r\n",'UTF-8'))
                #ndata = Relay.recv(24)
                self.Debugger.Log("Success!",PrintName=False)
            except:
                self.Debugger.Log("Failed!",PrintName=False)
                self.Debugger.Log("***Error: Failed to send data to Relay!****")
            finally:
                Relay.close
                self.send(bytes("ok",'UTF-8'))


class TCPS_SPOT(asyncore.dispatcher):

    #Server Variables
    IP = "192.168.1.102"
    Port = 7000
    BufferSize = 1024
    ConnectionLimit = 10
    
    def __init__(self):
        global IP, Port, BufferSize, ConnectionLimit
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((self.IP, self.Port))
        self.listen(self.ConnectionLimit)
        self.Debugger.Log("Listening on " + self.IP + ":" + str(self.Port) + "; Max Connections:" + str(self.ConnectionLimit) + " ...")
        

    def handle_accepted(self, sock, addr):
        self.Debugger.Log('Incoming connection from %s' % repr(addr))
        handler = TCPSHandler(sock)

server = TCPS_SPOT()
asyncore.loop()
