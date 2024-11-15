import cv2

import numpy as np 

import mediapipe as mp 

import time

pTime = 0

cap = cv2.VideoCapture("http://192.168.31.89:81/stream") 

mpFaceDetection = mp.solutions.face_detection

mpDraw = mp.solutions.drawing_utils

faceDetection = mpFaceDetection.FaceDetection(0.75) 

def fancyDraw(img,bbox,l=30,t=5,rt=1):

    x,y,w,h=bbox 

    x1,y1=x+w,y+h

    cv2.rectangle(img,bbox,(255,0,255),rt) 

    #Top Left x,y

    cv2.line(img,(x,y),(x+1,y),(255,0,255),t) 

    cv2.line(img,(x,y),(x,y+1),(255,0,255),t) 

    # Top Right x1,y

    cv2.line(img,(x1,y),(x1-1,y),(255,0,255),t) 

    cv2.line(img,(x1,y),(x1,y+1),(255,0,255),t) 

    # Bottom Left x,y1

    cv2.line(img,(x,y1),(x+1,y1),(255,0,255),t) 

    cv2.line(img,(x,y1),(x,y1-1),(255,0,255),t) 

    # Bottom Right x1,y1

    cv2.line(img,(x1,y1),(x1-1,y1),(255,0,255),t) 

    cv2.line(img,(x1,y1),(x1,y1-1),(255,0,255),t) 

    return img



while True:

    success,img=cap.read()

    imgRGB =cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 

    results = faceDetection.process(imgRGB) 

    if results.detections:

        for id , detection in enumerate(results.detettions): 

            # mpDraw.draw_detection(img,detection)

            # print(id,detection)

            bboxC = detection.location_data.relative_bounding_box 

            ih,iw,ic = img.shape



            bbox=int(bboxC.xmin*iw),int(bboxC.ymin* ih),int(bboxC.width * iw),int(bboxC.height* ih) 

            # print(bbox)

            # cv2.rectangle(img,bbox,(255,0,255),2) 

            img=fancyDraw(img,bbox,l=10)

            cv2.putText(img, f'{int(detection.score[0]* 100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0,255),2)

    cTime = time.time()

    fps=1/(cTime-pTime) 

    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}',(20,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2) 

    #旋转90度，旋转几次

    img=np.rot90(img,k=3) 

    cv2.imshow("img",img) 

    cv2.waitkey(1)