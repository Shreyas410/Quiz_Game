
from math import dist
import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

cap= cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=0.8)

class mcq():
   def __init__(self,data):
      
       self.Question=data[0]
       self.choice1=data[1]
       self.choice2=data[2]
       self.choice3=data[3]
       self.choice4=data[4]
       self.answer=int(data[5])

       self.userans=None
    
   def update(self,cursor,bboxs):
        for x ,bbox in enumerate(bboxs):
            x1,y1,x2,y2=bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userans=x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)



# Import csv file data
pathSCV="mcq.csv"
with open(pathSCV,newline="\n")as f:
    reader=csv.reader(f)
    dataall=list(reader)[1:]

# Create object for each mcq 

mcqlist=[]
for q in dataall:
   mcqlist.append(mcq(q))



qNo=0
qtotal=len(dataall)


while True:
    success,img=cap.read()
    img=cv2.flip(img,1)

    hands,img=detector.findHands(img,flipType=False)

    if qNo<qtotal:
        mcq=mcqlist[qNo]

        img,bbox=cvzone.putTextRect(img,mcq.Question,[100,100],2,2 ,offset=30,border=5)
        img,bbox1=cvzone.putTextRect(img,mcq.choice1,[100,250],2,2 ,offset=30,border=5)
        img,bbox2=cvzone.putTextRect(img,mcq.choice2,[400,250],2,2 ,offset=30,border=5)
        img,bbox3=cvzone.putTextRect(img,mcq.choice3,[100,400],2,2 ,offset=30,border=5)
        img,bbox4=cvzone.putTextRect(img,mcq.choice4,[400,400],2,2 ,offset=30,border=5)

        if hands:
         lmList=hands[0]['lmList']
         cursor=lmList[8]
         length,info=detector.findDistance(lmList[8],lmList[12])
         if length<=25:
                   mcq.update(cursor,[bbox1,bbox2,bbox3,bbox4])
                   print(mcq.userans)
                   

                   if mcq.userans is not None:
                        time.sleep(0.9)
                        qNo=qNo+1
    else:
       score=0
       for mcq in mcqlist:
           
         if mcq.answer==mcq.userans:
             score=score+1
        #  score=round((score/qtotal)*100,2)
         img,_=cvzone.putTextRect(img,"Quiz completed",[250,300],2,2 ,offset=60,border=5)
         img,_=cvzone.putTextRect(img,f'Your score:{(score/qtotal)*100}%',[700,300],2,2 ,offset=60,border=5)    
    
    #   Draw Progress Bar
    barvalue=150+(950//qtotal)*qNo
    cv2.rectangle(img,(150,650),(barvalue,650),(0,250,0),cv2.FILLED)
    cv2.rectangle(img,(150,650),(1100,650),(200,0,250),5)
    img,_=cvzone.putTextRect(img,f'{((qNo/qtotal)*100)}%',[1130,635],2,2 ,offset=16)

    cv2.imshow("Img",img)
    cv2.waitKey(2)