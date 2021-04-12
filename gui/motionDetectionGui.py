from PyQt5.QtWidgets import *
from designer_python import Ui_motiondetectclassifiy



import cv2
import numpy as np 

class firstGui(Ui_motiondetectclassifiy,QMainWindow):

    def __init__(self):
        super(firstGui,self).__init__()
        self.ui = Ui_motiondetectclassifiy()
        self.ui.setupUi()
        
        self.LoadNewVideo.clicked.connect(lambda: self.firstGui.play())
        self.Stop.clicked.connect(lambda: self.firstGui.stop())
        self.NextFrame.clicked.connect(lambda: self.firstGui.comingFrame())
        self.prevFrame.clicked.connect(lambda: self.firstGui.previousFrame())
        #self.LoadNewVideo.clicked.connect(lambda: self.firstGui.openNewClass())
        #self.LoadNewVideo.clicked.connect(lambda: self.firstGui.play())
        #self.LoadNewVideo.clicked.connect(lambda: self.firstGui.play())
        #self.LoadNewVideo.clicked.connect(lambda: self.firstGui.play())
        #self.LoadNewVideo.clicked.connect(lambda: self.firstGui.play())
        self.LoadVideo()

    def motionDetect(self,frame1,frame2,treshold):
        self.frame1 = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2GRAY)
        self.frame2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2GRAY)

        h, w = self.frame1.shape
        error = self.frame1-self.frame2
        error = np.sum(np.square(error))/(2*h*w)

        print(error)
        if error>self.treshold:
        
          return True 

    #def mom(self):
        
        
    
    def LoadVideo(self):
        path = "/home/hk/Desktop/seniorDesignProject/videoplayback.mp4"
        media = phonon.Phonon.MediaSource(path)

    
#    def stopVideo(self,stop):
#
#    
#    def previousFrame(self,prevFrame):
#
#    
#    def comingFrame(self,nextFrame):
#
#    
#    def comingFrame(self,nextFrame):
#
#
#    def saveFrame(self,SaveThisFrames):

if __name__ == "__main__":
    app = QApplication([])
    window=firstGui()
    window.show()
    app.exec()
