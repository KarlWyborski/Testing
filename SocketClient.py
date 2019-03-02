import socket
import threading
import sys
from datetime import datetime
import time
import tkinter
from tkinter import *
import os


def rcvMsg():
    global iAddTime
    global iCurrentTime
    global bSET
    global hourOffset
    global minOffset
    global secOffset
    
    data = 'a'
    b1 = True
    while b1:
        try:
            data = sock.recv(1024)
            if not data:
                break
            if data.decode('utf-8') == 'ConnTest':
                print('StillConnected')
            else:
                data = data.decode('utf-8').split('\n')
                print(data)
                max = 6
                if len(data) < max:
                    max = len(data)
                else:
                    pass
                i = 0
                # i = 0
                tempData = data[i].split(',')
                bSET = tempData[0]
                iAddTime = tempData[1]
                hourOffset = int(tempData[2])
                minOffset = int(tempData[3])
                secOffset = int(tempData[4])
                
                if bSET == 'True':
                    lAddTime.configure(text=str(iAddTime))
                else:
                    lAddTime.configure(text='')
                
                i += 1
                
                while i < max:
                    tempData = data[i].split(',')
                    print(i)
                    print(tempData)
                    
                    #formats minute
                    if int(tempData[5]) < 10:
                        tempData[5] = '0'+tempData[5]
                    
                    #formats hour and AM or PM
                    if int(tempData[4]) > 12:
                        lStamps[i-1].configure(text=str(int(tempData[4])-12) + ':' + tempData[5] +' PM')
                    elif int(tempData[4]) == 0:
                        lStamps[i-1].configure(text='12:' + tempData[5] + ' AM')
                    elif int(tempData[4]) < 12:
                        lStamps[i-1].configure(text=tempData[4]+ ':' + tempData[5] +' AM')
                    elif int(tempData[4]) == 12:
                        lStamps[i-1].configure(text='12:' + tempData[5] + ' PM')
                        
                    lTimes[i-1].configure(text=tempData[0] + ' - ' + str(int(tempData[0]) + 5))
                    i += 1
        except socket.timeout:
            print('socket.timeout')
            sock.close()
            b1=False
            connect()
        
        
            
            
            
        

def connect():
    global connState
    global sock
    connState = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10.0)
    while not connState:
        try:
            print('Connecting...')
            sock.connect((ipAddress, PORT))
            print('Connected')
            startRcvThread()
            connState = True
        except ConnectionRefusedError:
            print('Connection Failed. Retrying in 10...')
            time.sleep(10)
	except socket.timeout:
            print('Connetion Timeout. Rerying in 10...')
            time.sleep(10)

def startRcvThread():
    rcvThread = threading.Thread(target=rcvMsg)
    rcvThread.daemon = True
    rcvThread.start()
    print('Rcv Thread Started.')
    
##def startSendThread():
##    time.sleep(1)
##    sendThread = threading.Thread(target=sendMsg)
##    sendThread.daemon = True
##    sendThread.start()
##    print('Send Thread Started.')
    
def cleanup():
    sock.close()
    win.destroy()

def onKeyPress(event):
    key = event.keysym
##    print("You Pressed %s" % (key))
    if key == 'Prior':
        sendServer('DOWN')
    elif key == 'Next':
        sendServer('UP')
    elif key == 'H' or key == 'Escape':
        sendServer('SET')
    elif key == 'b':
        sendServer('OTHER')
    
def sendServer(msg):
    print('Sending: ' + msg)
    sock.send((msg).encode('utf-8'))

def startClockThread():
    clockThread = threading.Thread(target=clockChange)
    clockThread.daemon = True
    clockThread.start()
    print('clock Thread Started.')

def clockChange():
    while True:
        temp = adjustTime()
        
        if temp[3] > 12:
            hour = str(temp[3] - 12)
        elif temp[3] == 0:
            hour = '12'
        elif temp[3] < 10:
            hour = '0'+ str(temp[3])
        else:
            hour = str(temp[3])
        
        if temp[3] > 12:
            AMPM = ' PM'
        else:
            AMPM = ' AM'
        
        if temp[4] > 9:
            min = str(temp[4])
        else:
            min = '0' + str(temp[4])
        
        if temp[5] > 9:
            sec = str(temp[5])
        else:
            sec = '0' + str(temp[5])
        
        clock.configure(text=hour+':'+min+':'+sec+AMPM)
        time.sleep(0.2)
    

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
    
#--------------------------------------------------------
#Sets up TKinter window
win = Tk()

clock = Label(win, text="insert time", font = 'Times 70', bg='gray70')
clock.pack(side = BOTTOM, fill=X)

textCurrentTime = Label(win, bg='White', height=1, text='Current CO Time', font='Times 30')
textCurrentTime.pack(fill=X)

lCurrentTime = Label(win, bg='White', text="## - ##", font = 'Times 100')
lCurrentTime.pack(fill=X)

lAddTime = Label(win, bg='White', text="", font = 'Times 70')
lAddTime.pack(fill=X)

lCurrentStamp = Label(win, bg='pale green', height = 2, text="Updated at: HH:MM", font = 'Times 40')
lCurrentStamp.pack(fill=X)

lHistTime1 = Label(win, pady=15, bg='gray70', text="-- - --", font = 'Times 70')
lHistTime1.pack(fill=X)

lHistStamp1 = Label(win, pady=15, anchor=SE, bg='gray70', text="HH:MM", font = 'Times 40')
lHistStamp1.pack(fill=X)

lHistTime2 = Label(win, pady=15, bg='White', text="-- - --", font = 'Times 70')
lHistTime2.pack(fill=X)

lHistStamp2 = Label(win, pady=15, anchor=SE, bg='White', text="HH:MM", font = 'Times 40')
lHistStamp2.pack(fill=X)

lHistTime3 = Label(win, pady=15, bg='gray70', text="-- - --", font = 'Times 70')
lHistTime3.pack(fill=X)

lHistStamp3 = Label(win, pady=15, anchor=SE, bg='gray70', text="HH:MM", font = 'Times 40')
lHistStamp3.pack(fill=X)

lHistTime4 = Label(win, pady=15, bg='White', text="-- - --", font = 'Times 70')
lHistTime4.pack(fill=X)

lHistStamp4 = Label(win, pady=15, anchor=SE, bg='White', text="HH:MM", font = 'Times 40')
lHistStamp4.pack(fill=X)

lTimes = [lCurrentTime,lHistTime1,lHistTime2,lHistTime3,lHistTime4]
lStamps = [lCurrentStamp,lHistStamp1,lHistStamp2,lHistStamp3,lHistStamp4]
    
#-------------------------------------------------------
#Sets up socket connection
    

ipAddress = sys.argv[1]
PORT = 12343

sRequest = 'PlaceHolder'
connState = False
iAddTime = 0
iCurrentTime = 0
bSET = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10.0)
hourOffset=0
minOffset=0
secOffset=0


connect()
startClockThread()
##startSendThread()

win.protocol("WM_DELETE_WINDOW", cleanup)
win.bind('<Key>', onKeyPress)
win.mainloop()
