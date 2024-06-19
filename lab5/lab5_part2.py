import cv2
import numpy as np
import time
import os


classes = []
net = cv2.dnn.readNet('lab-1-SethBrand-sys/lab5/yolov5s.onnx')
with open("lab-1-SethBrand-sys/lab5/classes.txt") as f:
    for line in f:
        classes.append(line.strip())
def format_yolo5(frame):
    # put the image in square big enough
    col, row, _ = frame.shape
    _max = max(col,row) # get the maximum dimension
    resized = np.zeros((_max, _max, 3), np.uint8) # create a new square frame
    resized[0:col, 0:row] = frame # insert the original image at the top left
    # yolo works with images that have float pixels between 0 and 1, 640x640, RGB channels
    # opencv has byte pixels, BGR channels (by default)
    # the below function converts to the required format
    result = cv2.dnn.blobFromImage(resized, 1/255.0, (640,640), swapRB = True)
    return result

def process_frame(frame):
    blob = format_yolo5(frame) #convert yolo to input
    net.setInput(blob)
    predictions = net.forward() #run the network
    output = predictions[0] #we only provided one frame, so we get the first prediction
    #these three will hold
    boxes = []
    confidences = []
    class_ids = [] #we'll fill up these below
    for row in output: #each row in the output it one box, xc, yc, w, h, conf, 80 class probabilities
        if row[4] > 0.5: #we only keep boxes with good confidence
            xc, yc, w, h = row[0], row[1], row[2], row[3] #note these are 640x640 space
            max_index = cv2.minMaxLoc(row[5:])[3][1] #this will figure out the highest probability class
            class_ids.append(max_index)
            #figure out the location of the box
            left = int(xc-w/2)
            top = int(yc-h/2)
            width = int(w)
            height = int(h)
            #append the confidence and the box, because we'll need it
            confidences.append(row[4])
            boxes.append([left,top,width,height])


    #eliminate duplicate boxes with non-maximmum suppression (gives best box indexes)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)
    draw_boxes(frame, boxes, indexes, class_ids)
    true1 = False
    true2 = False
    true3 = False
    for i, f in enumerate(class_ids):
        if f == 0:
            true1 = True
        elif f == 39:
            true2 = True
        elif f == 67:
            true3 = True
    date = time.ctime()
    date = date.replace(':','-')
    print(date)
    
    if true1 and true2 and true3:
        picture = cv2.imwrite(f'lab-1-SethBrand-sys/lab5/{date}.jpg', frame)
        if picture:
            print("saved")
        else:
            print("failed to save")
        cap.release()
        cv2.destroyAllWindows()
    else:
        true1 = False
        true2 = False
        true3 = False
    

def draw_boxes(frame, boxes, indexes, class_ids):
    #now we draw in the original frame the best boxes
    sf = int(max(frame.shape[0], frame.shape[1])/640) # determine the scale factor to convert back
    for i in indexes:
        x,y,w,h = [v*sf for v in boxes[i]] #extract the box  multiplied by the scale factor
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),2) # draw a blue box
        cv2.putText(img = frame, #draw the class label in red
                    text = (classes[class_ids[i]]),
                    org = (x,y),
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale= 0.5, color = (0,0,255))


def main():
    global cap
    cap = cv2.VideoCapture(0) #0 is an index to the first camera
    while cap.isOpened():
        ret, frame = cap.read() #res will indicate success or failure, frame is a numpy array (360, 640). Oriented like that because of rows and columns orientation in numpy
        if not ret:
            continue #no frame read
        process_frame(frame)
        cv2.imshow("my window", frame) #quick gui
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break #exit loop when key q is pressed
        
    cap.release() #stop the camera
    cv2.destroyAllWindows() #closes the open gui window
    
    

if __name__ == "__main__":
    main()