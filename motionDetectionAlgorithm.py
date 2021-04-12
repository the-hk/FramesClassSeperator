import cv2
import numpy as np 


def motionDetect(frame1,frame2,treshold):
  frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
  frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

  h, w = frame1.shape
  error = frame1-frame2
  error = np.sum(np.square(error))/(2*h*w)
  
  print(error)
  if error>treshold:
    
    return True 

location = "/home/hk/Desktop/seniorDesignProject/videoplayback.mp4"
cap = cv2.VideoCapture(location)

frameCounter=0
frames=[]
ret, frame2= cap.read()
h, w, c = frame2.shape
frame1=np.array(frame2)

while(True):
  frameCounter = frameCounter + 1   
  
  ret, frame1 = cap.read()
  treshold=1


  if ret == True:
   
    
    cv2.imshow('Frame', frame1)
    if motionDetect(frame1,frame2,treshold):
      frames=np.append(frames,frameCounter)
      #print(frameCounter)

    frame2=frame1
   
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
   
  
  else: 
    break
   

print(frames)

cap.release()
   

cv2.destroyAllWindows()

