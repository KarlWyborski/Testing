import RPi.GPIO as GPIO
import time

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
            else:
                print("Carry out time can now be changed.\n")
                co_change = 1
        op_ts = time_now

def tick():
    global time1
    time1 = 0
    time2 = time.strftime('%I:%M:%S %p')
    print(time2)
    # if convert_time(time2) != time1:
    #     time1 = time2
    #     clockTime.configure(text = time2)
    #     clockTime.after(200, tick)
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





#tkinter setup
win = Tk()
win.title("Carry Out Time")
myFont = tkinter.font.Font(family = 'Helvetica',size = 24, weight = "bold")

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
co_time_label.configure(text = co_time, font = myFont)

##Buttons
testbutton = Button(botFrame, text = "EXIT", font = myFont, command = close, bg ='red')
testbutton.pack()
#while 1:
#    time.sleep(1)


try:
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
    
    
        
except KeyboardInterrupt:
    print("1\n")
    close()
    
except:
    print("2\n")
    close()
    
finally:
    print("End of program")
