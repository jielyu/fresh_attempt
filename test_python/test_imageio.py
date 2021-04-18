# encoding: utf-8
import os
import numpy as np
import matplotlib.pyplot as plt
import pylab
import imageio
import skimage.io
import numpy as np  
import cv2  

video_path = 'F://Download/Utorrent/Django.Unchained.2012.BluRay.ipad.720p.x264.AAC-BYRPAD.mp4'
print(os.path.isfile(video_path))
cap = cv2.VideoCapture(video_path)  
print(cap.isOpened())
while(cap.isOpened()):  
    ret, frame = cap.read()  
    #print(frame.shape)
    cv2.imshow('image', frame)  
    k = cv2.waitKey(20)  
    #q键退出
    if (k & 0xff == ord('q')):  
        break  

cap.release()  
cv2.destroyAllWindows()