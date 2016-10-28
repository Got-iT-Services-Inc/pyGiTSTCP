#############################################################
# Title: Python TCP Server Class                            #
# Description: Wrapper around TCP Server for easy handing   #
#              of TCP communications                        #
# Version:                                                  #
#   * Version 1.0 10/27/2016 RC                             #
#                                                           #
# Author: Richard Cintorino (c) Richard Cintorino 2015      #
#############################################################

import asyncore
import socket
from Debug import pyDebugger

class pyTCPServer():
