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
import subprocess
import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import scipy as sp
from scipy.io.wavfile import read
from scipy.io.wavfile import write    
from scipy import signal
import matplotlib.pyplot as plt


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
global totalframecount
global video_total_duration


filename = "sa"
storedFrames = np.zeros(10)
paused = False
FrameNumber=0
today = date.today()
root=Tk()
videoLoad = False

host ="/home/hk/Desktop/projects/Labeler_video_player_for_ML/videoplayback.mp4"#0 #"http://192.168.43.1:8080"
cap = cv2.VideoCapture(host)

def soundfilter(filename):
    (Frequency, array) = read(filename) # Reading the sound file.
    time = array/Frequency
    len(array) # length of the array
    FourierTransformation = sp.fft.fft(array) # FFT of signal
    scale = np.linspace(0, Frequency, len(array)) # Plot scaling
    b,a = signal.butter(6, 60/(Frequency/2), btype='highpass') # ButterWorth filter 4350
    filteredSignal = signal.lfilter(b,a,array)
    c,d = signal.butter(2, 2005/(Frequency/2), btype='lowpass') # ButterWorth lowpass-filter
    newFilteredSignal = signal.lfilter(c,d,filteredSignal) # Applying the filter to the signal
    newFilteredSignal = np.asarray(newFilteredSignal, dtype=np.int16)

    newFilteredSignal = newFilteredSignal * 100
    plt.plot(newFilteredSignal)
    name_of_the_sound, ext = os.path.splitext(filename)

    write(name_of_the_sound+"filtered"+ext, Frequency, newFilteredSignal) # Saving it to the file.
    if os.path.exists(filename):
        os.remove(filename)
        print("The file was deleted") 
    else:
        print("The file does not exist")  


def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


def cut_the_video(detected_time,input_name_path,output_name_path):
    if detected_time <5:
        start_time = 0
    else:
        start_time = detected_time-5
    end_time = detected_time + 5
    
    ffmpeg_extract_subclip(input_name_path, start_time, end_time, targetname=output_name_path)
    convert_video_to_audio_ffmpeg(output_name_path,output_ext="wav")



def convert_video_to_audio_ffmpeg(video_file,output_ext="wav"):
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    if os.path.exists(video_file):
        os.remove(video_file)
    else:
        print("The file does not exist")        

def selected_item():
    global classDir  
    # Traverse the tuple returned by
    # curselection method and print
    # correspoding value(s) in the listbox
    for i in lbox.curselection():
        print(lbox.get(i))
        classDir = lbox.get(i)
    
def callFolders():
    flist = os.listdir('/home/hk/Desktop/projects/Labeler_video_player_for_ML/classes/')
    a=0
    for item in flist:
        a=a+1
        lbox.insert(a, item) 
    lbox.grid()


def openNewClass_button_callback():
    directory="/home/hk/Desktop/projects/Labeler_video_player_for_ML/classes/"
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
    global filename
    global totalframecount
    global video_total_duration

    imDir=classDir
    newDir="/home/hk/Desktop/projects/Labeler_video_player_for_ML/classes/"+imDir+"/"+str(FrameNumber)+"frame"+str(today)+".jpg"
    
    cv2.imwrite(newDir,frame) 
    print("frame was saved")
    fps = totalframecount/video_total_duration
    detected_time = FrameNumber/fps
    output_name_path = "/home/hk/Desktop/projects/Labeler_video_player_for_ML/classes/"+imDir+"/"+str(FrameNumber)+"frame"+str(today)+".mp4"
    cut_the_video(detected_time,filename,output_name_path)
    output_name_path_for_filtered_signal = "/home/hk/Desktop/projects/Labeler_video_player_for_ML/classes/"+imDir+"/"+str(FrameNumber)+"frame"+str(today)+".wav"
    soundfilter(output_name_path_for_filtered_signal)

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
    

def loadVideo_button_callback():
    global filename
    global videoLoad
    global cap
    global totalframecount
    global video_total_duration

    filename = filedialog.askopenfilename(initialdir = "/home/hk/Desktop",title = "Select a File")
    totalframecount= int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_total_duration = get_length(filename)
    host = filename
    cap = cv2.VideoCapture(host)
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


flist = os.listdir('/home/hk/Desktop/projects/Labeler_video_player_for_ML/classes/')
 
lbox = Listbox(app2)


lbutton = Button(app2, text='change directory', command=selected_item)
  
# Placing the button and listbox
lbutton.grid()


#open_img()
if videoLoad==True:
    cap = cv2.VideoCapture(filename)
    video_stream()

root.mainloop()
