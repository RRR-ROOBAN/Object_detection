from django.contrib import admin
from django.shortcuts import render

def button(request):
    return render(request,'home.html')

def output(request):
    # import necessary modules
    import cv2
    import numpy as np
    classes='C:/Users/Demo/projects/objectclass/objectclass/coco.names'
    yolovcf='C:/Users/Demo/projects/objectclass/objectclass/yolov3.cfg'
    yolovweight='C:/Users/Demo/projects/objectclass/objectclass/yolov3.weights'
    # import the yolo detector file
    from yolo_detector import YoloDetector

    # read the default classes for the yolo model
    with open(classes, 'r') as f:
        classes = [w.strip() for w in f.readlines()]
    print("Default classes: \n")
    for n, cls in enumerate(classes):
        print("%d. %s" % (n+1, cls))
    # select specific classes that you want to detect out of the 80 and assign a color to each detection
    selected = {"person": (0, 255, 255),
                "laptop": (0, 0, 0)}
    # initialize the detector with the paths to cfg, weights, and the list of classes
    detector = YoloDetector(yolovcf, yolovweight, classes)
    # initialize video stream
    cap = cv2.VideoCapture("C:/Users/Demo/projects/objectclass/objectclass/input_video.mp4")
    # read first frame
    ret, frame = cap.read()
    # loop to read frames and update window
    while ret:
        # this returns detections in the format {cls_1:[(top_left_x, top_left_y, top_right_x, top_right_y), ..],
        #                                        cls_4:[], ..}
        # Note: you can change the file as per your requirement if necessary
        detections = detector.detect(frame)
        # loop over the selected items and check if it exists in the detected items, if it exists loop over all the items of the specific class
        # and draw rectangles and put a label in the defined color
        for cls, color in selected.items():
            if cls in detections:
                for box in detections[cls]:
                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=1)
                    cv2.putText(frame, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)
        # display the detections
        #cv2.imshow("detections", frame)
        # wait for key press
        key_press = cv2.waitKey(1) & 0xff
        # exit loop if q or on reaching EOF
        if key_press == ord('q'):
            break
        ret, frame = cap.read()
        return render(request,'home.html',cv2.imshow('detections',frame))
    
    # release resources
    cap.release()
    # destroy window
    cv2.destroyAllWindows()
    

# Register your models here.
