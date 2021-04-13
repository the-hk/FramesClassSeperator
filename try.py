from tkinter import *
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image
import pyscreenshot as ImageGrab
import pyautogui
import cv2
import os 

global cap
global root
global host
global result 

host = "/home/hk/Desktop/seniorDesignProject/videoplayback.mp4"#0 #"http://192.168.43.1:8080"
cap = cv2.VideoCapture(host)

    

def openNewClass_button_callback():
    directory="/home/hk/Desktop/seniorDesignProject/classes/"
    result=textExample.get("1.0","end")
    
    try:
        if not os.path.exists(directory+result):
            os.makedirs(directory+result)
            l = Label(lmain, text = " class was created", font = "Helvetica 20 bold italic" )
            l.grid(row = 20, column = 10)    
            l.after(1000,lambda: l.destroy())
    except :
        print ('Error: Creating directory')
        l = Label(lmain, text = 'Error: Creating directory. ' , font = "Helvetica 20 bold italic" )
        l.grid(row = 20, column = 10)    
        l.after(1000,lambda: l.destroy())




def ss_button_callback():
    print("screenshot was taken")
    im=ImageGrab.grab()#bbox=(500,10,1000,500)
    im.save(r"/home/hk/Desktop/seniorDesignProject/hk.png")
    l = Label(lmain, text = " screenshot was taken", font = "Helvetica 20 bold italic" )
    l.grid(row = 5, column = 10)    
    l.after(1000,lambda: l.destroy())

def play_button_callback():
    print("played")
    
    
    l = Label(lmain, text = " played", font = "Helvetica 20 bold italic" )
    l.grid(row = 5, column = 10)    
    l.after(1000,lambda: l.destroy())

def stop_button_callback():
    print("stopped")
    while play_button is False:
        a=a+1
    
    l = Label(lmain, text = " stopped", font = "Helvetica 20 bold italic" )
    l.grid(row = 5, column = 10)    
    l.after(1000,lambda: l.destroy())

def prevF_button_callback():
    print("previous frame")
    
    
    l = Label(lmain, text = " previous frame", font = "Helvetica 20 bold italic" )
    l.grid(row = 5, column = 10)    
    l.after(1000,lambda: l.destroy())

def nextF_button_callback():
    print("next frame")
  
  
    l = Label(lmain, text = " next frame", font = "Helvetica 20 bold italic" )
    l.grid(row = 5, column = 10)    
    l.after(1000,lambda: l.destroy())
 

def loadVideo_button_callback():
    print("loading video")
    
    
    l = Label(lmain, text = " video loaded", font = "Helvetica 20 bold italic" )
    l.grid(row = 5, column = 10)    
    l.after(1000,lambda: l.destroy())      


# function for video streaming
def video_stream():
    global cap
    global root

    ret, frame = cap.read()
    if ret is True:        
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        #img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(1, video_stream) 

    elif ret is False:
        openfn="/home/hk/Desktop/seniorDesignProject/hk.png"
        x = openfn
        img = Image.open(x)
        #img = img.resize((root.winfo_screenwidth()-70, root.winfo_screenheight()-200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        lmain.img = img
        lmain.configure(image = img) 
        cap = cv2.VideoCapture(host)
        lmain.after(1, video_stream)

root = Tk()
root.title("video laryngoscope")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))# Create a frame
root.configure(background='#787467')
#

#open_img()
app = LabelFrame(root, bg='#787467')
app.place(x = 0,y = 0)


# Create a label in the frame
lmain = Label(app, background='#787467')
lmain.grid()
lmain2 = Label(app, background='#787467')
lmain.grid(row = 3, column = 5)

# Capture from camera


#photo = PhotoImage(file = "/home/hk/Desktop/python_examples/inovar3.png" ) 

ss_button = Button(root, text = "screen shot", padx = 30, pady = 20, command = ss_button_callback,bg="yellow",font = "Helvetica 12 bold italic")
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
 
lbox = Listbox(root)

 
# THE ITEMS INSERTED WITH A LOOP
for item in flist:
    lbox.insert(END, item)
 
lbox.pack(side=TOP)


#open_img()
video_stream()
root.mainloop()