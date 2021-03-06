#! python3
import socket
import threading
import sys
from datetime import datetime
import time
import tkinter
from tkinter import *
import os
##import Tkinter.font

port = 12345

helv70 = ('Helvetica',70)
helv70B = ('Helvetica Bold',100)
helv30 = ('Helvetica', 30)
##win = Tk()
##helv36 = font.Font(family = 'Helvetica',size = 70)
##helv48B = tkFont.Font(family = 'Helvetica',size = 70, weight = "bold")

#Superclasses
class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    iCurrentTime = 0
    iCurrentStamp = 0
    iAddTime = 0
    bToggle = False
    sHistFileName = "/home/pi/DeweysProject/Testing/test.txt"
    
    def __init__(self):
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

class Client:
    
    def __init__(self, address):
        self.sRequest = 'PlaceHolder'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ipAddress = address
        
        self.startSendThread()
        self.connect()
    
    def sendMsg(self):
        while True:
            
            print(str(threading.active_count()) + 'in send thread')
            try:
                self.sock.send((self.sRequest).encode('utf-8'))
                print('Sending data Request: ' + self.sRequest)
            except BrokenPipeError as e:
                print('BrokenPipeError detected...')
                self.connState = False
                self.sock.close()
                time.sleep(1)
                self.connect()
            time.sleep(1)
    
    def rcvMsg(self):
        while True:
            self.data = self.sock.recv(1024)
            if not self.data:
                break
            print(str(self.data.decode('utf-8')))
            self.data = self.data.decode('utf-8')
    
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.ipAddress, port))
            self.startRcvThread()
            self.connState = True
        except ConnectionRefusedError as e:
            self.sock.close()
            print('Connection Failed. Retrying...')
            print(threading.active_count())
            time.sleep(10)
            self.connect()
    
    def startRcvThread(self):
        rcvThread = threading.Thread(target=self.rcvMsg)
        rcvThread.daemon = True
        rcvThread.start()
        print('Rcv Thread Started.')
    
    def startSendThread(self):
        sendThread = threading.Thread(target=self.sendMsg)
        sendThread.daemon = True
        sendThread.start()
        print('Send Thread Started.')
        
    
        

class BigWindow:
##    win = Tk()
##    leftFrame = Frame(win)
##    leftBottomFrame = Frame(leftFrame)
##    leftLeftFrame = Frame(leftFrame)
##    leftRightFrame = Frame(leftFrame)
##    rightFrame = Frame(win)
##    rightLeftFrame = Frame(rightFrame)
##    rightRightFrame = Frame(rightFrame)
##    clock = Label(leftBottomFrame)
##    lCurrentTime = Label(leftLeftFrame)
    def __init__(self):
        self.win = Tk()
        

        self.clock = Label(self.win, text="insert time", font = 'Times 70', bg='gray70')
        self.clock.pack(side = BOTTOM, fill=X)
        
        self.textCurrentTime = Label(self.win, bg='White', height=1, text='Current CO Time', font='Times 30')
        self.textCurrentTime.pack(fill=X)
        
        
        self.lCurrentTime = Label(self.win, bg='White', text="## - ##", font = 'Times 100')
        self.lCurrentTime.pack(fill=X)
        
        self.lAddTime = Label(self.win, bg='White', text="", font = 'Times 70')
        self.lAddTime.pack(fill=X)
        
        
        
        
        self.lCurrentStamp = Label(self.win, bg='pale green', height = 2, text="Updated at: HH:MM", font = 'Times 40')
        self.lCurrentStamp.pack(fill=X)
    ##        self.lCurrentStamp.grid(row=1,column=0)
        

        self.lHistTime1 = Label(self.win, pady=15, bg='gray70', text="-- - --", font = 'Times 70')
        self.lHistTime1.pack(fill=X)
        
        self.lHistStamp1 = Label(self.win, pady=15, anchor=SE, bg='gray70', text="HH:MM", font = 'Times 40')
        self.lHistStamp1.pack(fill=X)
        
        self.lHistTime2 = Label(self.win, pady=15, bg='White', text="-- - --", font = 'Times 70')
        self.lHistTime2.pack(fill=X)
        
        self.lHistStamp2 = Label(self.win, pady=15, anchor=SE, bg='White', text="HH:MM", font = 'Times 40')
        self.lHistStamp2.pack(fill=X)
        
        self.lHistTime3 = Label(self.win, pady=15, bg='gray70', text="-- - --", font = 'Times 70')
        self.lHistTime3.pack(fill=X)
        
        self.lHistStamp3 = Label(self.win, pady=15, anchor=SE, bg='gray70', text="HH:MM", font = 'Times 40')
        self.lHistStamp3.pack(fill=X)
        
        self.lHistTime4 = Label(self.win, pady=15, bg='White', text="-- - --", font = 'Times 70')
        self.lHistTime4.pack(fill=X)
        
        self.lHistStamp4 = Label(self.win, pady=15, anchor=SE, bg='White', text="HH:MM", font = 'Times 40')
        self.lHistStamp4.pack(fill=X)
        
        self.lHistTimes = [self.lHistTime1,self.lHistTime2,self.lHistTime3,self.lHistTime4]
        self.lHistStamps = [self.lHistStamp1,self.lHistStamp2,self.lHistStamp3,self.lHistStamp4]
        
        self.sHistTimes = [' ',' ',' ','' ,' ']
        self.sHistStamps = [' ',' ',' ',' ',' ']

class SmallWindow:
    
    def __init__(self):
        self.iCurrentTime = 0
        self.win = Tk()
        self.lCurrentTime = Label(self.win)
        self.lCurrentTime.pack()
        self.lCurrentTime.configure(text="## - ##", font = helv70B)
##        self.win.mainloop()
   
    

#Subclasses
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
class BigServer(Server, BigWindow):
    
    
    
    def __init__(self):
        Server.__init__ (self)
        BigWindow.__init__ (self)
        self.tick()
        self.loadHist()
        self.win.geometry("1024x1900")
        self.win.bind('<Key>', self.onKeyPress)
        
        self.win.mainloop()
        self.win.protocol('WM_DELETE_WINDOW', self.close)
    
    def close(self):
        pass
##        win.destroy()
    
    def onKeyPress(self, event):
        print("You Pressed %s" % (event.keysym, ))
        if event.keysym == "space":
            self.opButton()
        elif event.keysym == "Up":
            self.upButton()
        elif event.keysym == "Down":
            self.downButton()
        else:
            print("No function bound. \n")
        
    def upButton(self):
        if self.bToggle:
            self.iAddTime = self.iAddTime + 5
            self.lAddTime.configure(text=self.iAddTime)
    
    def downButton(self):
        if self.bToggle:
            if self.iCurrentTime+self.iAddTime < 16:
                pass
            else:
                self.iAddTime = self.iAddTime - 5
                self.lAddTime.configure(text=self.iAddTime)
    
    def opButton(self):
        print(self.iAddTime)
        if self.bToggle:
            self.bToggle = False
            self.lAddTime.configure(text='')
            if self.iAddTime != 0:
                self.iCurrentTime = self.iCurrentTime + self.iAddTime
                self.iAddTime = 0
                self.lCurrentTime.configure(text = str(self.iCurrentTime) + " - " + str(self.iCurrentTime+5))
                aTimeStamp = self.adjustTime()
                sToWrite = str(self.iCurrentTime)
                i = 0
                while i < 9:
                    sToWrite = sToWrite + ',' + str(aTimeStamp[i])
                    i+=1
                print(sToWrite)
                self.text_insert(self.sHistFileName,sToWrite + "\n")
                self.loadHist()
        else:
            self.bToggle = True
            self.lAddTime.configure(text=0)
    
    def adjustTime(self):
        hourOffset = 0
        minOffset = 5
        secOffset = 30
        inTime = [0,0,0,0,0,0,0,0,0]
        i = 0
        while i < 9:
            inTime[i] = time.localtime()[i]
            i += 1
        
        if (inTime[5] + secOffset) > 59:
            minOffset += 1
            inTime[5] = inTime[5] + secOffset - 60
        else:
            inTime[5] = inTime[5] + secOffset
        
        if (inTime[4] + minOffset) > 59:
            hourOffset += 1
            inTime[4] = inTime[4] + minOffset - 60
        else:
            inTime[4] = inTime[4] + minOffset
        
        inTime[3] = inTime[3] + hourOffset
        return inTime
    
    def loadHist(self):
        f = open(self.sHistFileName, "r")
        i = 0
        am_pm = 'AM'
        print(i)
        today = time.localtime()
        for l in f:
            l_sep = l.split(",",9)
            if (l_sep[1] == str(today[0])) and (l_sep[2] == str(today[1])) and (l_sep[3] == str(today[2])):
                if int(l_sep[4]) > 12:
                    l_sep[4] = str(int(l_sep[4]) - 12)
                    am_pm = "PM"
                elif int(l_sep[4]) == 12:
                    am_pm = "PM"
                elif int(l_sep[4]) == 0:
                    l_sep[4] = "12"
                else:
                    am_pm = "AM"
                    
                if int(l_sep[5]) < 10:
                    l_sep[5] = "0" + l_sep[5]
                
                if i == 0:
                    self.iCurrentTime = int(l_sep[0])
                    self.lCurrentTime.configure(text = str(self.iCurrentTime) + " - " + str(self.iCurrentTime+5))
                    self.lCurrentStamp.configure(text = 'Updated at: ' + l_sep[4] + ":" + l_sep[5] + "  " + am_pm)
                    
                    self.sHistTimes[i] = str(self.iCurrentTime) + " - " + str(self.iCurrentTime+5)
                    self.sHistStamps[i] = 'Updated at: ' + l_sep[4] + ":" + l_sep[5] + "  " + am_pm
                    
                    i += 1
                elif i < 5:
                    print("fixing hist row " + str(i))
                    self.lHistTimes[i-1].configure(text = l_sep[0] + " - " + str(int(l_sep[0])+5))
                    self.lHistStamps[i-1].configure(text = l_sep[4] + ":" + l_sep[5] + "  " + am_pm)
                    
                    self.sHistTimes[i] = l_sep[0] + " - " + str(int(l_sep[0])+5)
                    self.sHistStamps[i] = l_sep[4] + ":" + l_sep[5] + "  " + am_pm
                    
                    i += 1
                
            else:
                pass
            
            f.close
            if i == 0:
                print('No data for today found. Creating new itme.')
                self.iCurrentTime = 10
                self.iAddTime = 5
                self.bToggle = True
                self.opButton()
                i += 1
    
    def tick(self):
        callTime = self.adjustTime()
        AmPm = 'AM'
        if callTime[3] > 12:
            callTime[3] = callTime[3] - 12
            AmPm = 'PM'
        elif callTime[3] == 12:
            AmPm = 'PM'
        elif callTime[3] == 0:
            callTime[3] = 12
        else:
            pass
        
        if callTime[4] < 10 and callTime[5] < 10:
            self.clock.configure(text = str(callTime[3]) + ':0' + str(callTime[4]) + ':0' + str(callTime[5]) + ' ' + AmPm)
        elif callTime[4] < 10:
            self.clock.configure(text = str(callTime[3]) + ':0' + str(callTime[4]) + ':' + str(callTime[5]) + ' ' + AmPm)
        elif callTime[5] < 10:
            self.clock.configure(text = str(callTime[3]) + ':' + str(callTime[4]) + ':0' + str(callTime[5]) + ' ' + AmPm)
        else:
            self.clock.configure(text = str(callTime[3]) + ':' + str(callTime[4]) + ':' + str(callTime[5]) + ' ' + AmPm)
            
        self.clock.after(100,self.tick)
    
    def text_insert(self,originalfilename,string):
        with open(originalfilename,'r') as f:
            with open('newfile.txt','w') as f2: 
                f2.write(string)
                f2.write(f.read())
        os.rename('newfile.txt',originalfilename)

class BigClient(Client, BigWindow):
    def __init__ (self, address):
        self.data = 'self.data'
        Client.__init__ (self, address)
        BigWindow.__init__ (self)
        self.sRequest = 'FullHist'
        self.startUpdateThread()
        self.win.mainloop()
    
    def startUpdateThread(self):
        updateThread = threading.Thread(target=self.updateWin)
        updateThread.daemon = True
        updateThread.start()
        print('Update Thread Started.')
    
    def updateWin(self):
        while True:
            print('win Tick')
            iCurrentTime = self.data
            print('Printing iCurrentTime')
            print(iCurrentTime)
            print(type(iCurrentTime))
            if self.connState:
                self.lCurrentTime.configure(bg='White')
            else:
                self.lCurrentTime.configure(bg='Red')
            if self.data != 'self.data' and type(self.data) == type('data'):
                l_sep = self.data.split(',')
                i = 0
                while i < 5:
                    if i == 0:
                        self.lCurrentTime.configure(text=l_sep[i])
                    else:
                        self.lHistTimes[i-1].configure(text=l_sep[i])
                    i += 1
                while i < 10:
                    if i == 5:
                        self.lCurrentStamp.configure(text=l_sep[i])
                    else:
                        self.lHistStamps[i-6].configure(text=l_sep[i])
                    i += 1
            time.sleep(1)

class SmallClient(Client, SmallWindow):
    
    def __init__ (self, address):
        self.data = 'self.data'
        Client.__init__ (self, address)
        SmallWindow.__init__ (self)
        self.sRequest = 'CurrentTime'
        self.startUpdateThread()
        self.win.mainloop()
    
    def startUpdateThread(self):
        updateThread = threading.Thread(target=self.updateWin)
        updateThread.daemon = True
        updateThread.start()
        print('Update Thread Started.')
    
    def updateWin(self):
        while True:
            print('win Tick')
            iCurrentTime = self.data
            print('Printing iCurrentTime')
            print(iCurrentTime)
            print(type(iCurrentTime))
            if self.connState:
                self.lCurrentTime.configure(bg='White')
            else:
                self.lCurrentTime.configure(bg='Red')
            if self.data != 'self.data' and type(self.data) == type('data'):
                self.lCurrentTime.configure(text = (iCurrentTime + ' - ' + str(int(iCurrentTime) + 5)))
            time.sleep(1)


    
if (len(sys.argv) > 1):
    if sys.argv[2] == 'small':
        client = SmallClient(sys.argv[1])
    elif sys.argv[2] == 'big':
        client = BigClient(sys.argv[1])
##    client.run()
##elif (len(sys.argv) == 2):
##    client = ClientBig(sys.argv[1])
##    client.run()
else:
    server = BigServer()
##    server.run()
