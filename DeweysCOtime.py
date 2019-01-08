import time
import os
import socket
from threading import Thread
from datetime import datetime

from tkinter import *
import tkinter.font

###Defined Funtcion
def onKeyPress(event):
    print("You Pressed %s\n" % (event.keysym, ))
    if event.keysym == "space":
        op_button()
    elif event.keysym == "Up":
        up_button()
    elif event.keysym == "Down":
        down_button()
    else:
        print("No function bound. \n")
          
def up_button():
    global up_ts
    global co_time
    global temp_co_change
    time_now = time.time()
    if ((time_now - up_ts) > 0.3) and co_change:
        temp_co_change = temp_co_change + 5
        print(temp_co_change)
        addTime.configure(text=temp_co_change)
    up_ts = time_now
        
def down_button():
    global down_ts
    global co_time
    global temp_co_change
    time_now = time.time()
    if ((time_now - down_ts) > 0.3) and co_change:
        if (co_time + temp_co_change) < 16:
            print("Carry out time cannot be less than 15-20 minutes.\n")
        else:
            temp_co_change = temp_co_change - 5
            print(temp_co_change)
            addTime.configure(text=temp_co_change)
    down_ts = time_now
        
def op_button():
    global op_ts
    global co_time
    global co_change
    global temp_co_change
    time_now = time.time()
    if (time_now - op_ts) > 0.3:
        print(temp_co_change)
        if co_change:
            print("Carry out time has been changed.\n")
            addTime.configure(text='')
            co_change = 0
            co_time = co_time + temp_co_change
            temp_co_change = 0
            print(co_time)
            currentTime.configure(text = str(co_time) + " - " + str(co_time+5))
            time_stamp = time.localtime()
            #writes CO time
            str_to_write = str(co_time)
            print(str_to_write)
            i = 0
            while i < 9:
                str_to_write = (str_to_write + "," + str(time_stamp[i]))
                i += 1
            print(str_to_write)
            text_insert(file_name,str_to_write + "\n")
            load_history()
        else:
            print("Carry out time can now be changed.\n")
            addTime.configure(text=0)
            co_change = 1
        #op_ts =

def text_insert(originalfilename,string):
    with open(originalfilename,'r') as f:
        with open('newfile.txt','w') as f2: 
            f2.write(string)
            f2.write(f.read())
    os.rename('newfile.txt',originalfilename)

def load_history():
    f = open(file_name, "r")
    i = 0
    for l in f:
        l_sep = l.split(",",9)
        print(l_sep)
        if int(l_sep[4]) > 12:
            l_sep[4] = str(int(l_sep[4]) - 12)
            print(l_sep[4])
            am_pm = "PM"
            print(am_pm)
        elif int(l_sep[4]) == 12:
            am_pm = "PM"
        elif int(l_sep[4]) == 0:
            l_sep[4] = "12"
        else:
            am_pm = "AM"
        
        if int(l_sep[5]) < 10:
            l_sep[5] = "0" + l_sep[5]
        
        if i == 0:
            co_time = l_sep[0]
            currentTime.configure(text = co_time + " - " + str(int(co_time)+5))
            currentStamp.configure(text = l_sep[4] + ":" + l_sep[5] + "  " + am_pm)
            i += 1
        elif i < 5:
            histTimes[i-1].configure(text = l_sep[0] + " - " + str(int(l_sep[0])+5))
            histStamps[i-1].configure(text = l_sep[4] + ":" + l_sep[5] + "  " + am_pm)
            i += 1
        

def tick():
    global time1
    time1 = 0
    time2 = time.strftime('%I:%M:%S %p')
    if time2 != time1:
        time1 = time2
        clockTime.configure(text = time2)
        clockTime.after(200,tick)
        
        
    
    
#Runs at end of script
def close():
    win.destroy()


#Varialbes
pos_offset = 0
global co_time
co_time = 15
global temp_co_change
temp_co_change = 0

up_ts = time.time()
down_ts = up_ts
op_ts = up_ts

co_change = 0

file_name = "test.txt"



#tkinter setup
win = Tk()
win.title("Carry Out Time")
myFont = tkinter.font.Font(family = 'Helvetica',size = 48, weight = "bold")
clockFont = tkinter.font.Font(family = 'Helvetica',size = 36)
currentFont = tkinter.font.Font(family = 'Helvetica',size = 48, weight = "bold")
histFont = tkinter.font.Font(family = 'Helvetica',size = 36)
otherFont = tkinter.font.Font(family = 'Helvetica',size = 24)

###Widgets
##Frames
topFrame = Frame(win)
topFrame.pack(pady=30)
midFrame = Frame(win)
midFrame.pack()
midLeftFrame = Frame(midFrame)
midLeftFrame.pack(side = LEFT, padx=30)
midRightFrame = Frame(midFrame)
midRightFrame.pack(side = RIGHT, padx=30)
botFrame = Frame(win)
botFrame.pack()

##Labels
clockTime = Label(botFrame)
clockTime.pack(side = LEFT, padx=30, pady=30)
clockTime.configure(text="insert time", font = clockFont)

currentTime = Label(topFrame)
currentTime.pack(side = TOP)
currentTime.configure(text="## - ##", font = currentFont)
currentStamp = Label(topFrame)
currentStamp.pack(side = BOTTOM)
currentStamp.configure(text="HH:MM", font = currentFont)
addTime = Label(topFrame)
addTime.pack(side = RIGHT)
addTime.configure(text="", font = clockFont)

histTime1 = Label(midLeftFrame)
histTime1.pack()
histTime1.configure(text="## - ##", font = histFont)
histStamp1 = Label(midRightFrame)
histStamp1.pack()
histStamp1.configure(text="HH:MM", font = histFont)
histTime2 = Label(midLeftFrame)
histTime2.pack()
histTime2.configure(text="HH:MM", font = histFont)
histStamp2 = Label(midRightFrame)
histStamp2.pack()
histStamp2.configure(text="HH:MM", font = histFont)
histTime3 = Label(midLeftFrame)
histTime3.pack()
histTime3.configure(text="HH:MM", font = histFont)
histStamp3 = Label(midRightFrame)
histStamp3.pack()
histStamp3.configure(text="HH:MM", font = histFont)
histTime4 = Label(midLeftFrame)
histTime4.pack()
histTime4.configure(text="HH:MM", font = histFont)
histStamp4 = Label(midRightFrame)
histStamp4.pack()
histStamp4.configure(text="HH:MM", font = histFont)

histTimes = [histTime1,histTime2,histTime3,histTime4]
histStamps = [histStamp1,histStamp2,histStamp3,histStamp4]

##seperators

##Buttons
testbutton = Button(botFrame, text = "EXIT", font = otherFont, command = close, bg ='red')
testbutton.pack(side = RIGHT, padx=30, pady=30)
#while 1:
#    time.sleep(1)


try:
    load_history()
    co_time = int(currentTime.cget("text")[:2])
    print(currentTime.cget("text")[:2])
    
    win.bind('<Key>',onKeyPress)
    
    tick()
    
##    send_thread = Thread(target=send)
##    send_thread.start()
    
    win.mainloop()
    win.protocol('WM_DELETE_WINDOW', close)

except KeyboardInterrupt:
    print("1\n")
    close()
    
except:
    print("2\n")
    close()
    
finally:
    print("End of program")


