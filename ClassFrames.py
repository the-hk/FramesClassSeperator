from tkinter import *
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image
import pyscreenshot as ImageGrab
import pyautogui
import cv2
import os 
from datetime import date
import numpy as np

global cap
global root
global host
global result 
global classDir  
global FrameNumber
global today
global frame 
global paused
global storedFrames
global filename
global videoLoad


filename = "sa"
storedFrames = np.zeros(10)
paused = False
FrameNumber=0
today = date.today()
root=Tk()
videoLoad = False

host ="/home/hk/Desktop/seniorDesignProject/videoplayback.mp4"#0 #"http://192.168.43.1:8080"
cap = cv2.VideoCapture(host)

        

def selected_item():
    global classDir  
    # Traverse the tuple returned by
    # curselection method and print
    # correspoding value(s) in the listbox
    for i in lbox.curselection():
        print(lbox.get(i))
        classDir = lbox.get(i)
    
def callFolders():
    flist = os.listdir('/home/hk/Desktop/seniorDesignProject/classes/')
    a=0
    for item in flist:
        a=a+1
        lbox.insert(a, item) 
    lbox.grid()


def openNewClass_button_callback():
    directory="/home/hk/Desktop/seniorDesignProject/classes/"
    result=textExample.get("1.0","end")
    lbox.delete(0,tkinter.END)
    
    try:
        if not os.path.exists(directory+result):
            os.makedirs(directory+result)
            l = Label(lmain, text = " class was created", font = "Helvetica 20 bold italic" )
            l.grid(row = 20, column = 10)    
            l.after(1000,lambda: l.destroy())
    except :
        print ('Error: Creating directory')
        #l = Label(lmain, text = 'Error: Creating directory. ' , font = "Helvetica 20 bold italic" )
        #l.grid(row = 20, column = 10)    
        #l.after(1000,lambda: l.destroy())
    callFolders()    




def ss_button_callback():
    global classDir
    global FrameNumber
    global today
    global frame

    print("frame was saved")
    imDir=classDir
    newDir="/home/hk/Desktop/seniorDesignProject/classes/"+imDir+"/"+str(FrameNumber)+"frame"+str(today)+".jpg"
    
    #im=ImageGrab.grab()#bbox=(500,10,1000,500)
    #im.save(newDir)
    cv2.imwrite(newDir,frame) 
    #l = Label(lmain, text = " screenshot was taken", font = "Helvetica 20 bold italic" )
    #l.grid(row = 5, column = 10)    
    #l.after(1000,lambda: l.destroy())

def play_button_callback():
    global paused


    print("played")
    
    paused = False
    return paused
    

def stop_button_callback():
    global paused

    print("stopped")
   
    paused = True
    return paused
    

def prevF_button_callback():

    print("previous frame")
    
    global cap
    global root
    global FrameNumber
    global frame
    global paused

    cap.set(cv2.CAP_PROP_POS_FRAMES, FrameNumber)
    ret, frame = cap.read()
    if ret is True:        
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        FrameNumber=FrameNumber-2
        #img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    elif ret is False: 
        cap = cv2.VideoCapture(host)
    
    
    #l = Label(lmain, text = " previous frame", font = "Helvetica 20 bold italic" )
    #l.grid(row = 5, column = 10)    
    #l.after(1000,lambda: l.destroy())

def nextF_button_callback():
    global cap
    global root
    global FrameNumber
    global frame
    global paused

    print("next frame")
    cap.set(cv2.CAP_PROP_POS_FRAMES, FrameNumber)
    ret, frame = cap.read()
    if ret is True:        
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        FrameNumber=FrameNumber+1
        #img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    elif ret is False:
        cap = cv2.VideoCapture(host)
    
  
    #l = Label(lmain, text = " next frame", font = "Helvetica 20 bold italic" )
    #l.grid(row = 5, column = 10)    
    #l.after(1000,lambda: l.destroy())
 

def loadVideo_button_callback():
    global filename
    global videoLoad

    filename = filedialog.askopenfilename(initialdir = "/home/hk/Desktop",title = "Select a File")
    video_stream()
    videoLoad = True
    
    #l = Label(lmain, text = " video loaded", font = "Helvetica 20 bold italic" )
    #l.grid(row = 5, column = 10)    
    #l.after(1000,lambda: l.destroy())      


# function for video streaming
def video_stream():
    global cap
    global root
    global FrameNumber
    global frame
    global paused
    if paused is False:
        ret, frame = cap.read()
        if ret is True:        
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            FrameNumber=FrameNumber+1
            #img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(1, video_stream) 
        elif ret is False:
            lmain.after(1, video_stream)
    else:
        lmain.after(1, video_stream)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))# Create a frame
root.configure(background='#787467')
# 

#open_img()
app = LabelFrame(root, bg='#787467')
app.pack(side=TOP)

app2 = LabelFrame(root, bg='#787467')
app2.pack(side=BOTTOM)

# Create a label in the frame
lmain = Label(app, background='#787467')
lmain.grid()
lmain2 = Label(app, background='#787467')
lmain.grid(row = 3, column = 5)

# Capture from camera


#photo = PhotoImage(file = "/home/hk/Desktop/python_examples/inovar3.png" ) 

ss_button = Button(root, text = "save frame", padx = 30, pady = 20, command = ss_button_callback,bg="yellow",font = "Helvetica 12 bold italic")
ss_button.pack(side=RIGHT,expand=True)
#
play_button = Button(root, text = "play", padx = 30, pady = 20, command = play_button_callback,bg="yellow",font = "Helvetica 12 bold italic")
play_button.pack(side=RIGHT)
#
stop_button= Button(root, text = "stop", padx = 30, pady = 20, command = stop_button_callback,bg="yellow",font = "Helvetica 12 bold italic")
stop_button.pack(side=RIGHT)
#
prevFrame_button= Button(root, text = "previous frame", padx = 30, pady = 20, command = prevF_button_callback,bg="yellow",font = "Helvetica 12 bold italic")
prevFrame_button.pack(side=RIGHT)
#
nextFrame_button= Button(root, text = "next frame", padx = 30, pady = 20, command = nextF_button_callback,bg="yellow",font = "Helvetica 12 bold italic")
nextFrame_button.pack(side=RIGHT)
#
loadVideo_button= Button(root, text = "load video", padx = 30, pady = 20, command = loadVideo_button_callback,bg="yellow",font = "Helvetica 12 bold italic")
loadVideo_button.pack(side=RIGHT)
#
openNewClass_button= Button(root, text = "open new class", padx = 30, pady = 20, command = openNewClass_button_callback,bg="yellow",font = "Helvetica 12 bold italic")
openNewClass_button.pack(side=RIGHT)
#
textExample=Text(root,height=1)
textExample.pack(side=RIGHT)


flist = os.listdir('/home/hk/Desktop/seniorDesignProject/classes/')
 
lbox = Listbox(app2)


lbutton = Button(app2, text='change directory', command=selected_item)
  
# Placing the button and listbox
lbutton.grid()


#open_img()
if videoLoad==True:
    cap = cv2.VideoCapture(filename)
    video_stream()

root.mainloop()