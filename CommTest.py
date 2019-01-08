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
myFont = tkFont.Font(family = 'Helvetica',size = 48, weight = "bold")

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
        
        self.topFrame = Frame(win)
        self.topFrame.pack(pady=30)
        self.midFrame = Frame(win)
        self.midFrame.pack()
        self.midLeftFrame = Frame(self.midFrame)
        self.midLeftFrame.pack(side = LEFT, padx=30)
        self.midRightFrame = Frame(self.midFrame)
        self.midRightFrame.pack(side = RIGHT, padx=30)
        self.botFrame = Frame(win)
        self.botFrame.pack()

        #Label Settings
        self.clock = Label(self.botFrame)
        self.clock.pack(side = LEFT, padx=30, pady=30)
        self.clock.configure(text="insert time", font = myFont)
        
        self.lCurrentTime = Label(self.topFrame)
        self.lCurrentTime.pack(side = TOP)
        self.lCurrentTime.configure(text="## - ##", font = myFont)
        self.lCurrentStamp = Label(self.topFrame)
        self.lCurrentStamp.pack(side = BOTTOM)
        self.lCurrentStamp.configure(text="HH:MM", font = myFont)
        self.lAddTime = Label(self.topFrame)
        self.lAddTime.pack(side = RIGHT)
        self.lAddTime.configure(text="", font = myFont)

        self.histTime1 = Label(self.midLeftFrame)
        self.histTime1.pack()
        self.histTime1.configure(text="## - ##", font = myFont)
        self.histStamp1 = Label(self.midRightFrame)
        self.histStamp1.pack()
        self.histStamp1.configure(text="HH:MM", font = myFont)
        self.histTime2 = Label(self.midLeftFrame)
        self.histTime2.pack()
        self.histTime2.configure(text="HH:MM", font = myFont)
        self.histStamp2 = Label(self.midRightFrame)
        self.histStamp2.pack()
        self.histStamp2.configure(text="HH:MM", font = myFont)
        self.histTime3 = Label(self.midLeftFrame)
        self.histTime3.pack()
        self.histTime3.configure(text="HH:MM", font = myFont)
        self.histStamp3 = Label(self.midRightFrame)
        self.histStamp3.pack()
        self.histStamp3.configure(text="HH:MM", font = myFont)
        self.histTime4 = Label(self.midLeftFrame)
        self.histTime4.pack()
        self.histTime4.configure(text="HH:MM", font = myFont)
        self.histStamp4 = Label(self.midRightFrame)
        self.histStamp4.pack()
        self.histStamp4.configure(text="HH:MM", font = myFont)
        
        self.histTimes = [self.histTime1,self.histTime2,self.histTime3,self.histTime4]
        self.histStamps = [self.histStamp1,self.histStamp2,self.histStamp3,self.histStamp4]

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
            print("Carry out time has been changed.")
            self.lAddTime.configure(text='')
            self.iCurrentTime = self.iCurrentTime + self.iAddTime
            self.iAddTime = 0
            self.lCurrentTime.configure(text = str(self.iCurrentTime) + " - " + str(self.iCurrentTime+5))
            aTimeStamp = time.localtime()
            print(aTimeStamp)
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
    
    def loadHist(self):
        f = open(self.sHistFileName, "r")
        i = 0
        am_pm = 'AM'
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
                    i += 1
                elif i < 5:
                    print("fixing hist row " + str(i))
                    self.histTimes[i-1].configure(text = l_sep[0] + " - " + str(int(l_sep[0])+5))
                    self.histStamps[i-1].configure(text = l_sep[4] + ":" + l_sep[5] + "  " + am_pm)
                    i += 1
                
            else:
                pass
            
            f.close
            if i == 0:
                self.iCurrentTime = 15
                self.bToggle = True
                self.opButton()
    
    def tick(self):
        self.clock.configure(text = time.strftime('%I:%M:%S %p'))
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
            data = c.recv(1024)
            if data.encode('utf-8') == 'CurrentTime':
                c.send(str(self.iCurrentTime).encode('utf-8'))
            else:
                c.send(('I got:').encode('utf-8') + data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                c.close()
                break

    

class Client:
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
        lCurrentTime.configure(text="## - ##", font = myFont)
        
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
    client = Client(sys.argv[1])
    client.run()
else:
    server = Server()
    server.run()
