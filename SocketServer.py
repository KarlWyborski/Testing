import socket
import threading
import sys
from datetime import datetime
import time
import tkinter
from tkinter import *
import os


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []
iCurrentTime = 0
iCurrentStamp = 0
iAddTime = 0
bToggle = False
sHistFileName = "/home/pi/DeweysProject/Testing/test.txt"


self.sock.bind(('0.0.0.0', 12345))
self.sock.listen(1)
self.startAccThread()

##----------
def startAccThread(self):
    accThread = threading.Thread(target=self.acceptor)
    accThread.daemon = True
    accThread.start()

def acceptor(self):
    while True:
        c, a = self.sock.accept()
        cThread = threading.Thread(target=self.handler, args=(c,a))
        cThread.daemon = True
        cThread.start()
        self.connections.append(c)
        print(str(a[0]) + ':' + str(a[1]), "connected")

def handler(self, c, a):
    while True:
        data = c.recv(1024).decode('utf-8')
        print(data)
        if data == 'CurrentTime':
            
            c.send(str(self.iCurrentTime).encode('utf-8'))
        elif data == 'FullHist':
            c.send((self.sHistTimes[0] + ',' + self.sHistTimes[1] + ',' + self.sHistTimes[2] + ',' + self.sHistTimes[3] + ',' + self.sHistTimes[4]
                   + ',' + self.sHistStamps[0] + ',' + self.sHistStamps[1] + ',' + self.sHistStamps[2] + ',' + self.sHistStamps[3] + ',' + self.sHistStamps[4]).encode('utf-8'))
##                c.send(sHistStamps[0] + ',' + sHistStamps[1] + ',' + sHistStamps[2] + ',' + sHistStamps[3] + ',' + sHistStamps[4])
        else:
            c.send(('I got:' + data).encode('utf-8'))
        if not data:
            print(str(a[0]) + ':' + str(a[1]), "disconnected")
            self.connections.remove(c)
            c.close()
            break
