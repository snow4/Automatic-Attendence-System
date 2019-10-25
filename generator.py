import cv2
import numpy as np
import dlib
import sqlite3
import os

cap = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def InsertOrUpdate(id,Name):
    conn = sqlite3.connect("Face.db")
    cmd = "Select * FROM Student WHERE ID = "+str(id)
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if(isRecordExist==1):
        cmd = "UPDATE Student SET Name"+str(Name)+"WHERE ID="+str(id)
    else:
        cmd = "INSERT INTO Student(ID,Name) Values("+str(id)+","+str(Name)+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()

id = input("enter your id")
name = input("enter your name")

InsertOrUpdate(id, name)

sampleNum = 0
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        sampleNum = sampleNum+1
        cv2.imwrite("dataset/User."+str(id)+"."+str(sampleNum)+".jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        
        cv2.waitKey(100)
        
    cv2.imshow('img', img)
    cv2.waitKey(30) & 0xFF 

    
    if (sampleNum>20):
        break

cap.release()
cv2.destroyAllWindows()
