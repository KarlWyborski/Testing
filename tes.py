import RPi.GPIO as GPIO
import time
import os

from datetime import datetime

from tkinter import *
import tkinter.font

###Defined Funtcion
def up_button(channel):
    if GPIO.input(11):
        global up_ts
        global co_time
        global temp_co_change
        time_now = time.time()
        if ((time_now - up_ts) > 0.3) and co_change:
            temp_co_change = temp_co_change + 5
            print(temp_co_change)
        up_ts = time_now
        
def down_button(channel):
    if GPIO.input(7):
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
        down_ts = time_now
        
def op_button(channel):
    if GPIO.input(13):
        global op_ts
        global co_time
        global co_change
        global temp_co_change
        time_now = time.time()
        if (time_now - op_ts) > 0.3:
            print(temp_co_change)
            if co_change:
                print("Carry out time has been changed.\n")
                co_change = 0
                co_time = co_time + temp_co_change
                temp_co_change = 0
                print(co_time)
                co_time_label.configure(text = str(co_time) + " - " + str(co_time+5))
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
        else:
            am_pm = "AM"
            
        if i == 0:
            co_time = l_sep[0]
            co_time_label.configure(text = co_time + " - " + str(int(co_time)+5))
            i += 1
        elif i < 5:
            hist_times[i-1].configure(text = l_sep[0] + " - " + str(int(l_sep[0])+5)
                                    + "                      "
                                    + l_sep[4] + ":" + l_sep[5] + "  " + am_pm)
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
    print("GPIO Cleaned\n")
    GPIO.cleanup()
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

###Widgets
##Frames
topFrame = Frame(win)
topFrame.pack()
midFrame = Frame(win)
midFrame.pack()
botFrame = Frame(win)
botFrame.pack()

##Labels
clockTime = Label(topFrame)
clockTime.pack()
clockTime.configure(text="insert time", font = myFont)
co_time_label = Label(topFrame)
co_time_label.pack()
co_time_label.configure(text = str(co_time) + " - " + str(co_time+5), font = myFont)

hist_time1 = Label(midFrame)
hist_time1.pack()
hist_time1.configure(text="## - ##     HH:MM", font = myFont)
hist_time2 = Label(midFrame)
hist_time2.pack()
hist_time2.configure(text="## - ##     HH:MM", font = myFont)
hist_time3 = Label(midFrame)
hist_time3.pack()
hist_time3.configure(text="## - ##     HH:MM", font = myFont)
hist_time4 = Label(midFrame)
hist_time4.pack()
hist_time4.configure(text="## - ##     HH:MM", font = myFont)

hist_times = [hist_time1,hist_time2,hist_time3,hist_time4]
              
##seperators

##Buttons
testbutton = Button(botFrame, text = "EXIT", font = myFont, command = close, bg ='red')
testbutton.pack()
#while 1:
#    time.sleep(1)


try:
    load_history()
    #Pin Setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(11, GPIO.RISING, callback=up_button)
    GPIO.add_event_detect(7 , GPIO.RISING, callback=down_button)
    GPIO.add_event_detect(13, GPIO.RISING, callback=op_button)
    
    
    
    
    tick()
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
