import socket
import threading
import sys
from datetime import datetime
import time
import tkinter
from tkinter import *
import os




##----------
def startAccThread():
    accThread = threading.Thread(target=acceptor)
    accThread.daemon = True
    accThread.start()

def acceptor():
    global connections
    
    while True:
        c, a = sock.accept()
        cThread = threading.Thread(target=handler, args=(c,a))
        cThread.daemon = True
        cThread.start()
        connections.append(c)
        print(str(a[0]) + ':' + str(a[1]), "connected")

def handler(c, a):
    time.sleep(2)
    c.send((str_allData()).encode('utf-8'))
    while True:
        data = c.recv(1024).decode('utf-8')
        print(data)
        if data == 'UP':
            on_UP()
        elif data == 'DOWN':
            on_DOWN()
        elif data == 'SET':
            on_SET()
        else:
            pass
        if not data:
            print(str(a[0]) + ':' + str(a[1]), "disconnected")
            connections.remove(c)
            c.close()
            break

def broadcast(msg):
    for c in connections:
        c.send(msg.encode('utf-8'))

def on_UP():
    global iAddTime
    if bSET:
        iAddTime += 5
        broadcast(str_allData())

def on_DOWN():
    global iAddTime
    if bSET:
        iAddTime -= 5
        broadcast(str_allData())

def on_SET():
    global bSET
    global iAddTime
    global iCurrentTime
    global fullHistData
    if bSET:
        bSET=False
        if iAddTime != 0:
            iCurrentTime += iAddTime
            iAddTime = 0
            timeStamp = adjustTime()
            strToWrite = str(iCurrentTime)
            for i in timeStamp:
                strToWrite += ',' + str(i)
            strToWrite += '\n'
            text_insert(dataPath + '/' + fileName, strToWrite)
            f = open(dataPath + '/' + fileName, 'r')
            fullHistData = f.read()
            f.close()
    else:
        bSET=True
    broadcast(str_allData())
    

def text_insert(originalfilename,string):
        with open(originalfilename,'r') as f:
            with open('newfile.txt','w') as f2: 
                f2.write(string)
                f2.write(f.read())
        os.rename('newfile.txt',originalfilename)

#------------
def checkData():
    global fileName
    global iCurrentTime
    global fullHistData
    
    year = str(time.localtime()[0])
    
    if time.localtime()[1] < 10:
        month = '0' + str(time.localtime()[1])
    else:
        month = str(time.localtime()[1])
        
    if time.localtime()[2] < 10:
        day = '0' + str(time.localtime()[2])
    else:
        day = str(time.localtime()[2])
                        
    fileName = year + '_' + month + '_' + day + '.txt'
    if not os.path.isdir(dataPath):
        os.mkdir(dataPath)
        print('Creating ./data folder...')
        
    try:
        f = open(dataPath + '/' + fileName, 'r')
        print('File for today was found.')
    except FileNotFoundError:
        print('File for today not found. Creating new file...')
        f = open(dataPath + '/' + fileName, 'w')
        f.write('15')
        stamp = time.localtime()
        for i in stamp:
            f.write(',' + str(i))
    fullHistData = f.read()
    print(fullHistData)
    iCurrentTime = int(fullHistData.split('\n')[0].split(',')[0])
    print(iCurrentTime)
    f.close()
        
def adjustTime():
    tempHour = 0
    tempMin = 0
    
    inTime = [0,0,0,0,0,0,0,0,0]
    i = 0
    while i < 9:
        inTime[i] = time.localtime()[i]
        i += 1
    
    if (inTime[5] + secOffset) > 59:
        tempMin = 1
        inTime[5] = inTime[5] + secOffset - 60
    elif (inTime[5] + secOffset) < 0:
        tempMin = -1
        inTime[5] = inTime[5] + secOffset + 60
    else:
        inTime[5] = inTime[5] + secOffset
    
    if (inTime[4] + minOffset + tempMin) > 59:
        tempHour = 1
        inTime[4] = inTime[4] + minOffset + tempMin - 60
    elif (inTime[4] + minOffset + tempMin) < 0:
        tempHour = -1
        inTime[4] = inTime[4] + minOffset + tempMin + 60
    else:
        inTime[4] = inTime[4] + minOffset + tempMin
    
    inTime[3] = inTime[3] + hourOffset + tempHour
    return inTime

def str_allData():
    allData = str(bSET)+','+ str(iAddTime)+','+str(hourOffset)+','+str(minOffset)+','+str(secOffset)+'\n'
    allData = allData +  fullHistData
    return allData
    
    

#--------------------------------------------------------
#GLOABL VARIABLES
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []
iAddTime = 0
iCurrentTime = 0
bSET = False

    #Clock offset CONSTANTS
hourOffset = 0
minOffset = 5
secOffset = 30

dataPath = './data'
fileName = 'PLACEHOLDER'
fullHistData = ''




checkData()
sock.bind(('0.0.0.0', 12343))
sock.listen(1)
startAccThread()
try:
    print('Running socket server...')
    while True:
        pass
except KeyboardInterrupt:
    print('\nUser Interrupt')
    sock.close()
    