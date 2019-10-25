import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pickle as cPickle
import sqlite3
import time
P_Students = []
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
path = "dataset"

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer\\trainingData.yml")

def getProfile(ID):
    
    conn = sqlite3.connect("Face.db")
    cmd = "SELECT * FROM Student WHERE ID="+str(ID)
    cursor = conn.execute(cmd)
    
    profile = None
    
    for row in cursor:
        profile = row
        #print(profile)
        
    conn.close()
    return profile

dtime = time.asctime()
f = open('Report.txt','a+')
f.write(" \n")
f.write(str(dtime)+" \n")
f.write(" \n")
f.write("ID                  Name \n")
f.close()


def insertProfile(id,Name):
    
    if id in P_Students:
        pass
    
    else:
        f = open('Report.txt','a+')
        f.writelines(str(id)+"                 " +str(Name)+"\n")
        f.close()
        
    P_Students.append(id)   
##    conn = sqlite3.connect("Report.db")
##    cmd = "Select * FROM ATTENDENCE WHERE ID = "+str(id)
##    cursor = conn.execute(cmd)
##    isRecordExist = 0
##    for row in cursor:
##        isRecordExist = 1
##    if(isRecordExist==1):
##        cmd = "UPDATE ATTENDENCE SET Name"+str(Name)+"WHERE ID="+str(id)
##    else:
##        cmd = "INSERT INTO ATTENDENCE(ID,NAME) Values("+str(id)+","+str(Name)+")"
##    conn.execute(cmd)
##    conn.commit()
##    conn.close()
        

cap = cv2.VideoCapture(1)
fontface = cv2.FONT_HERSHEY_COMPLEX_SMALL
fontscale = 1
fontcolor = (255, 255, 255)
re = 0
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        
        ID,conf = recognizer.predict(gray[y:y+h,x:x+w])
        print(conf)
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        #print(ID)
        #threshold =140

        profile = getProfile(ID)
        if(profile!=None):
            cv2.putText(img, str(profile[0]), (x,y+h+30), fontface, fontscale, fontcolor )
            cv2.putText(img, str(profile[1]), (x,y+h+50), fontface, fontscale, fontcolor )
            cv2.putText(img, str(profile[2]), (x,y+h+70), fontface, fontscale, fontcolor )
            #print(profile[1])
            re=1
            
            
        else:
            cv2.putText(img, str("Unknown"), (x,y+h+30), fontface, fontscale, fontcolor )
            re = 0

    if re==1:
        insertProfile(profile[0],profile[1])
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xFF 

    if k == 27 :
        break

cap.release()
cv2.destroyAllWindows()
