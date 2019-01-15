import socket
import threading
import sys
from datetime import datetime
import time
import Tkinter
import tkFont
from Tkinter import *
import os
##import Tkinter.font




win = Tk()
helv36 = tkFont.Font(family = 'Helvetica',size = 70)
helv48B = tkFont.Font(family = 'Helvetica',size = 70, weight = "bold")

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    iCurrentTime = 0
    iCurrentStamp = 0
    iAddTime = 0
    bToggle = False
    sHistFileName = "/home/pi/TEST/test.txt"
    
    ## Tkinter Settings
    #Font Settings
    
    #Frame Settings
    
    
    
    win.title("Carry Out Time")
    
    
    def __init__(self):
        self.sock.bind(('0.0.0.0', 10002))
        self.sock.listen(1)
        
        self.leftFrame = Frame(win)
        self.leftFrame.pack(side = LEFT)
        
        self.leftBottomFrame = Frame(self.leftFrame)
        self.leftBottomFrame.pack(side=BOTTOM)
        
        
        self.leftLeftFrame = Frame(self.leftFrame)
        self.leftLeftFrame.pack(side=LEFT)
        self.leftRightFrame = Frame(self.leftFrame)
        self.leftRightFrame.pack(side=RIGHT)
        
        
        
##        self.rightFrame = Frame(win, width=950, height=1024)
        
##        self.rightFrame.pack(side = RIGHT)
        self.rightFrame = Frame(win)
        self.rightFrame.pack(side=RIGHT)
        self.rightLeftFrame = Frame(self.rightFrame)
        self.rightLeftFrame.pack(side=LEFT)
        self.rightRightFrame = Frame(self.rightFrame)
        self.rightRightFrame.pack(side=RIGHT)
        
##        
##        self.topFrame = Frame(win)
##        self.topFrame.pack(pady=30)
##        self.midFrame = Frame(win)
##        self.midFrame.pack()
##        self.midLeftFrame = Frame(self.midFrame)
##        self.midLeftFrame.pack(side = LEFT, padx=30)
##        self.midRightFrame = Frame(self.midFrame)
##        self.midRightFrame.pack(side = RIGHT, padx=30)
##        self.botFrame = Frame(win)
##        self.botFrame.pack()

        #Label Settings
        self.clock = Label(self.leftBottomFrame)
        self.clock.pack(side = BOTTOM, padx=30, pady=30)
##        self.clock.grid(row=2,column=0)
        self.clock.configure(text="insert time", font = helv36)
        
        self.lCurrentTime = Label(self.leftLeftFrame, anchor=W, width = 7, height = 1)
        self.lCurrentTime.pack(side = TOP, anchor = W)
##        self.lCurrentTime.grid(row=0,column=0)
        self.lCurrentTime.configure(text="## - ##", font = helv48B)
        self.lCurrentStamp = Label(self.leftRightFrame)
        self.lCurrentStamp.pack(side = TOP)
##        self.lCurrentStamp.grid(row=1,column=0)
        self.lCurrentStamp.configure(text="HH:MM", font = helv48B, anchor = NE, width = 8, height = 2)
        self.lAddTime = Label(self.leftLeftFrame)
        self.lAddTime.pack(side = TOP)
##        self.lAddTime.grid(row=0,column=1)
        self.lAddTime.configure(text="", font = helv48B)

        self.lHistTime1 = Label(self.rightLeftFrame, width = 8, pady=15, anchor = W)
        self.lHistTime1.pack()
        self.lHistTime1.configure(text="-- - --", font = helv36)
        self.lHistStamp1 = Label(self.rightRightFrame, pady=15)
        self.lHistStamp1.pack()
        self.lHistStamp1.configure(text="HH:MM", font = helv36)
        self.lHistTime2 = Label(self.rightLeftFrame, width = 8, pady=15, anchor = W)
        self.lHistTime2.pack()
        self.lHistTime2.configure(text="-- - --", font = helv36)
        self.lHistStamp2 = Label(self.rightRightFrame, pady=15)
        self.lHistStamp2.pack()
        self.lHistStamp2.configure(text="HH:MM", font = helv36)
        self.lHistTime3 = Label(self.rightLeftFrame, width = 8, pady=15, anchor = W)
        self.lHistTime3.pack()
        self.lHistTime3.configure(text="-- - --", font = helv36)
        self.lHistStamp3 = Label(self.rightRightFrame, pady=15)
        self.lHistStamp3.pack()
        self.lHistStamp3.configure(text="HH:MM", font = helv36)
        self.lHistTime4 = Label(self.rightLeftFrame, width = 8, pady=15, anchor = W)
        self.lHistTime4.pack()
        self.lHistTime4.configure(text="-- - --", font = helv36)
        self.lHistStamp4 = Label(self.rightRightFrame, pady=15)
        self.lHistStamp4.pack()
        self.lHistStamp4.configure(text="HH:MM", font = helv36)
        
        self.lHistTimes = [self.lHistTime1,self.lHistTime2,self.lHistTime3,self.lHistTime4]
        self.lHistStamps = [self.lHistStamp1,self.lHistStamp2,self.lHistStamp3,self.lHistStamp4]
        
        self.sHistTimes = [' ',' ',' ','' ,' ']
        self.sHistStamps = [' ',' ',' ',' ',' ']
        
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
                    self.lCurrentStamp.configure(text = l_sep[4] + ":" + l_sep[5] + "  " + am_pm)
                    
                    self.sHistTimes[i] = str(self.iCurrentTime) + " - " + str(self.iCurrentTime+5)
                    self.sHistStamps[i] = l_sep[4] + ":" + l_sep[5] + "  " + am_pm
                    
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
            
    def run(self):
        accThread = threading.Thread(target=self.acceptor)
        accThread.daemon = True
        accThread.start()
        
        
        
        
        
        self.tick()
        self.loadHist()
        win.geometry("1900x1024")
        win.bind('<Key>', self.onKeyPress)
        
        win.mainloop()
        win.protocol('WM_DELETE_WINDOW', self.close)
        
        
##        while True:
##            pass
        
 
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
            data = c.recv(1024).encode('utf-8')
            if data == 'CurrentTime':
                c.send(str(self.iCurrentTime).encode('utf-8'))
            elif data == 'FullHist':
                c.send(self.sHistTimes[0] + ',' + self.sHistTimes[1] + ',' + self.sHistTimes[2] + ',' + self.sHistTimes[3] + ',' + self.sHistTimes[4])
                c.send(self.sHistStamps[0] + ',' + self.sHistStamps[1] + ',' + self.sHistStamps[2] + ',' + self.sHistStamps[3] + ',' + self.sHistStamps[4])
            else:
                c.send(('I got:').encode('utf-8') + data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                c.close()
                break

    

class ClientSmall:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def sendMsg(self):
        while True:
            self.sock.send(('CurrentTime').encode('utf-8'))
            time.sleep(1)
    
    def rcvMsg(self, lCurrentTime, iCurrentTime):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data.encode('utf-8')))
            iCurrentTime = int(str(data.encode('utf-8')))
            lCurrentTime.configure(text = str(iCurrentTime) + ' - ' + str(iCurrentTime + 5))
    
    def __init__(self, address):
        self.sock.connect((address, 10002))
        iCurrentTime = 0
        
        lCurrentTime = Label(win)
        lCurrentTime.pack()
        lCurrentTime.configure(text="## - ##", font = helv48B)
        
        sendThread = threading.Thread(target=self.sendMsg)
        sendThread.daemon = True
        sendThread.start()
        
        rcvThread = threading.Thread(target=self.rcvMsg, args=(lCurrentTime, iCurrentTime))
        rcvThread.daemon = True
        rcvThread.start()
        
        
        
        
                
        win.mainloop()
        win.protocol('WM_DELETE_WINDOW', self.close)

        
    def run(self):
        pass
        
class ClientBig:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def sendMsg(self):
        while True:
            self.sock.send(('FullHist').encode('utf-8'))
            print('send')
            time.sleep(1)
    
    def rcvMsg(self, lCurrentTime, iCurrentTime):
        while True:
            data = self.sock.recv(1024)
            print('recieved')
            if not data:
                break
            print(str(data.encode('utf-8')))
            iCurrentTime = int(str(data.encode('utf-8')))
            lCurrentTime.configure(text = str(iCurrentTime) + ' - ' + str(iCurrentTime + 5))
    
    def __init__(self, address):
        self.sock.connect((address, 10002))
        iCurrentTime = 0
        
        lCurrentTime = Label(win)
        lCurrentTime.pack()
        lCurrentTime.configure(text="## - ##", font = helv48B)
        
        sendThread = threading.Thread(target=self.sendMsg)
        sendThread.daemon = True
        sendThread.start()
        
        rcvThread = threading.Thread(target=self.rcvMsg, args=(lCurrentTime, iCurrentTime))
        rcvThread.daemon = True
        rcvThread.start()
        
        
        
        
                
        win.mainloop()
        win.protocol('WM_DELETE_WINDOW', self.close)

        
    def run(self):
        pass
    
    

    
if (len(sys.argv) > 1):
    client = ClientSmall(sys.argv[1])
    client.run()
##elif (len(sys.argv) == 2):
##    client = ClientBig(sys.argv[1])
##    client.run()
else:
    server = Server()
    server.run()
