import cv2
import mediapipe as mp
import numpy as np
import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import threading
import struct
import time
import keyboard

global stop
global running
global bottom
global top
global start
global y


stop = False
start = 0
top = 0
bottom = 0
num = 0



a = struct.Struct("<hh")


running = True

global button
global count
count = 0
button = 0


#start by reading our pre-treained model
net = cv2.dnn.readNet('lab-1-SethBrand-sys/lab5/yolov5s.onnx')
#and the strings that correspond to each class ID (0-79)

classes = []
with open("lab-1-SethBrand-sys/lab5/classes.txt") as f:
    for line in f:
        classes.append(line.strip())


def async_thread():
    
    async def run():
        scanner = BleakScanner()
        devices = await scanner.discover(5,return_adv=True)
        print(devices)
        def notification_callback(sender,payload):
            global button
            global count
            button, count = a.unpack(payload)
            print(button, count)
            return button, count
            

        async with BleakClient("E8:9F:6D:09:2B:FA") as client:

            await client.start_notify("b0bb55cf-e0f0-4b05-8bca-c6a5835c7a02", notification_callback)
            while running:
                await asyncio.sleep(1)
                
                
            
    asyncio.run(run())

def camera_thread():
    async def run():
        await asyncio.sleep(7)
        
       
        

        def process_frame(frame, pose_results):
            for l in pose_results.landmark:
                x,y = int(l.x*frame.shape[1]), int(l.y*frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                
                
            
            
            cv2.putText(frame, f"Count: {count}", org=(0,20),fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale= 0.5, color = (0,0,255))
            cv2.putText(frame, f"Button Status: {button}", org=(0,40),fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale= 0.5, color = (0,0,255))
            
            
            print(frame.shape) #print (y,x,z of frame)
            

        def detect_pose(frame):
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detection = mp.solutions.pose.Pose()
            results = detection.process(image)
            return results
        
        
            
            
        def main():
            global cap
            squatCount = 0
            cap = cv2.VideoCapture(0) #0 is an index to the first camera
            difference = 0
            bottom = 0
            top = 0
            while cap.isOpened():
                ret, frame = cap.read() #res will indicate success or failure, frame is a numpy array (360, 640). Oriented like that because of rows and columns orientation in numpy
                if not ret:
                    continue #no frame read

                

                results = detect_pose(frame)
                
                if results.pose_landmarks:
                    leftKnee = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE]
                    rightKnee = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_KNEE]
                    leftAnkle = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ANKLE]
                    rightAnkle = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE]

                    Nose = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.NOSE]




                    kneeDist = leftKnee.y - rightKnee.y
                    ankleDist = leftAnkle.y - rightAnkle.y
                    if kneeDist > ankleDist:
                        cv2.putText(frame, f"Standing", org=(0,60),fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale= 0.5, color = (0,0,255))

                    elif kneeDist < ankleDist:
                        cv2.putText(frame, f"Squatting", org=(0,60),fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale= 0.5, color = (0,0,255))
                        
                    if button == 1:
                        if count == 1:
                            top = Nose.x
                        if count == 2:
                            bottom = Nose.x
                            

                        if count == 3:
                            break
                    
                    
                            
                    process_frame(frame, results.pose_landmarks)

                
                
                
                cv2.imshow("Exercise Repetition Counter", frame)
                if cv2.waitKey(1) == ord("q"):
                    break
                
            
            
            cap.release() #stop the camera
            cv2.destroyAllWindows() #closes the open gui window

        

        if __name__ == "__main__":
            main()
    asyncio.run(run())
    




M5Thread = threading.Thread(target = async_thread)
CameraThread = threading.Thread(target = camera_thread)

M5Thread.start()
CameraThread.start()

while running:
    time.sleep(1)
    if keyboard.read_key() == "q":
        running = False
    if running == False:
        time.sleep(2)
        M5Thread.join()
        CameraThread.join()
        