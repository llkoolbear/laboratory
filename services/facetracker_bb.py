#!/usr/bin/env python3
progname = "facetracker_bb.py"
ver = "ver 0.69"

# ===============================================================================
#
# Name:       facetracker_bb.py 
#
# Purpose:    Program for tracking face with camera and two servo gimbal
#
# Author:     Bear Bissen
#
# Created:    April 24, 2022
# Last Rev:   
# Edited by:  
#
# License: MIT Open License
#
# ===============================================================================

# import the necessary python libraries
import io
import time
import cv2 as cv
from threading import Thread
from devices.servos.gimbal import Gimbal
from imutils.video import WebcamVideoStream, FPS
import imutils

# Color data for OpenCV Markings
BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)

class Camera(WebcamVideoStream):

    # Camera Settings
    CAMERA_SRC = 0         
    CAMERA_WIDTH = 640     
    CAMERA_HEIGHT = 480    
    CAMERA_CENTER_X = int(CAMERA_WIDTH/2)
    CAMERA_CENTER_Y = int(CAMERA_HEIGHT/2)
    PIXELS_PER_DEGREE_X = CAMERA_WIDTH/60
    PIXELS_PER_DEGREE_Y = CAMERA_HEIGHT/30

    CAMERA_FRAMERATE = 30
    CAMERA_HFLIP = True    
    CAMERA_VFLIP = False

    # OpenCV Motion Tracking Settings
    MIN_AREA = 2000       # sq pixels - exclude all motion contours less than or equal to this Area
    THRESHOLD_SENSITIVITY = 25
    BLUR_SIZE = 10    

    def __init__(self, src=CAMERA_SRC):
        super().__init__(src)
        # Set the camera resolution to 640x480
        self.stream.set(cv.CAP_PROP_FRAME_WIDTH, self.CAMERA_WIDTH) 
        self.stream.set(cv.CAP_PROP_FRAME_HEIGHT, self.CAMERA_HEIGHT)
        # Set the camera frame rate to 30fps
        self.stream.set(cv.CAP_PROP_FPS, self.CAMERA_FRAMERATE)
        self.img = None
        self.previous_img = None

        self.motion_found = False
        self.motion_center_x = None
        self.motion_center_y = None

        self.face_found = False
        self.face_corner_x = None
        self.face_corner_y = None
        self.face_center_x = None
        self.face_center_y = None
        self.face_width = None
        self.face_height = None
        self.face_area = None

        # Load the cascade model
        models_path = '/home/bearbissen/repos/opencv/data/haarcascades/'
        frontal_face_model = models_path + 'haarcascade_frontalface_default.xml'
        self.face_classifier = cv.CascadeClassifier(frontal_face_model)

    def stop_camera(self):
        self.stop()
        cv.destroyAllWindows()

    def detect_motion(self):
        self.motion_found = False
        self.motion_center_x = None
        self.motion_center_y = None
        if self.img is not None and self.previous_img is not None:
            # Convert frame to grayscale
            gray_img_1 = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
            gray_img_2 = cv.cvtColor(self.previous_img, cv.COLOR_BGR2GRAY)
            biggest_area = self.MIN_AREA
            # Process images to see if there is motion
            differenceimage = cv.absdiff(gray_img_1, gray_img_2)
            differenceimage = cv.blur(differenceimage, (self.BLUR_SIZE,self.BLUR_SIZE))
            # Get threshold of difference image based on THRESHOLD_SENSITIVITY variable
            retval, thresholdimage = cv.threshold(differenceimage, self.THRESHOLD_SENSITIVITY, 255, cv.THRESH_BINARY)
            # Get all the contours found in the thresholdimage
            try:
                thresholdimage, contours, hierarchy = cv.findContours( thresholdimage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE )
            except:
                contours, hierarchy = cv.findContours( thresholdimage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE )  
            if contours != ():    # Check if Motion Found
                self.motion_found = True
                for c in contours:
                    found_area = cv.contourArea(c) # Get area of current contour
                    if found_area > biggest_area:   # Check if it has the biggest area
                        biggest_area = found_area   # If bigger then update biggest_area
                        (mx, my, mw, mh) = cv.boundingRect(c)    # get motion contour data
                        self.motion_center_x = int(mx + mw/2)
                        self.motion_center_y = int(my + mh/2)
                        print("detect_motion - Found Motion at px cx,cy (%i, %i) Area w%i x h%i = %i sq px" % (int(mx + mw/2), int(my + mh/2), mw, mh, biggest_area))
            else:
                print("detect_motion - No Motion Found")
                
        print('detect_motion - No Images Found')

    def detect_face(self):
        biggest_face = None
        biggest_face_area = 0
        self.face_found = False
        self.face_corner_x = None
        self.face_corner_y = None
        self.face_center_x = None
        self.face_center_y = None
        self.face_width = None
        self.face_height = None
        self.face_area = None
        if self.img is not None:
            gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
            # Detect the faces
            faces = self.face_classifier.detectMultiScale(gray, 1.1, 4)
            # Draw the rectangle around each face
            if faces != ():
                self.face_found = True
                for (x, y, w, h) in faces:
                    cv.rectangle(self.img, (x, y), (x+w, y+h), BLUE, 2)
                    if w*h > biggest_face_area:
                        #biggest_face = (x, y, w, h)
                        biggest_face_area = w*h
                        #(self.face_corner_x, self.face_corner_y, self.face_width, self.face_height) = biggest_face
                        self.face_corner_x = x
                        self.face_corner_y = y
                        self.face_width = w
                        self.face_height = h
                        self.face_center_x = int(self.face_corner_x + self.face_width/2)
                        self.face_center_y = int(self.face_corner_y + self.face_height/2)
                        self.face_area = self.face_width*self.face_height
                        cv.rectangle(self.img, (self.face_corner_x, self.face_corner_y), (self.face_corner_x+self.face_width, self.face_corner_y+self.face_height), GREEN, 2)
                        print("detect_face - Found Face at px cx,cy (%i, %i) Area w%i x h%i = %i sq px" % 
                            (self.face_center_x, self.face_center_y, self.face_width, self.face_height, self.face_area))
            else:
                print("detect_face - No Face Found")
        print('detect_face - No Images Found')
class FaceTracker():

    PAN_PIN = 17 #11
    TILT_PIN = 27 #13
    CAM_SRC = 0

    START_X = 0
    START_Y = 5
    MOVE_X = 2
    MOVE_Y = 1
        
    def __init__(self):

        # Display Settings
        self.debug = True        # Set to False for no data display
        self.verbose = True      # Add extra detailed information
        self.show_fps = True     # show frames per second processing speed
        self.window_on = True   # Set to True displays opencv windows (GUI desktop reqd)
        self.diff_window_on = False  # Show OpenCV image difference window
        self.thresh_window_on = False  # Show OpenCV image Threshold window

        # Initialize the gimbal
        print("initialize - Initializing gimbal")
        self.gimbal = Gimbal(self.PAN_PIN,self.TILT_PIN)
        self.gimbal.pan_goto(self.START_X,self.START_Y)

        # Initialize the camera
        print("initialize - Initializing camera")
        self.camera = Camera(self.CAM_SRC)
        self.camera.start()

    def track_face(self):

        while not self.camera.stopped:
            
            self.camera.img = self.camera.read()
            self.camera.detect_face()
            if self.camera.face_found:
                if self.debug:
                    print("track_face - Found Face at px cx,cy (%i, %i) Area w%i x h%i = %i sq px" % (self.camera.face_center_x, self.camera.face_center_y, self.camera.face_width, self.camera.face_height, self.camera.face_area))
                self.pan_to_pixel(self.camera.face_center_x, self.camera.face_center_y)
                if self.debug:
                    print(f"track_face - Panned to ({self.gimbal.x}, {self.gimbal.y})")
            else:
                print("track_face - No Face Found, Looking for Motion")
                self.camera.detect_motion()
                if self.camera.motion_found:
                    if self.debug:
                        print(f"track_face - Motion found at ({self.camera.motion_center_x},{self.camera.motion_center_x}) pixels")
                    self.pan_to_pixel(self.camera.motion_center_x, self.camera.motion_center_y)
                    if self.debug:
                        print(f"track_face - Panned to ({self.gimbal.x},{self.gimbal.y})")
                else:
                    if self.debug:
                        print("track_face - No motion found, beginning pan search")
                    self.gimbal.pan_search(self.MOVE_X,self.MOVE_Y)
                    if self.debug:
                        print(f"track_face - Panned to ({self.gimbal.x},{self.gimbal.y})")
            
            if cv.waitKey(1) == ord('q'):
                break
            if self.camera.img is not None:
                cv.imshow('img', self.camera.img)
                self.camera.previous_img = self.camera.img  # set previous frame for next iteration

    def pan_to_pixel(self, pixel_x, pixel_y):
        pan_dx = int((self.camera.CAMERA_CENTER_X - pixel_x) / self.camera.PIXELS_PER_DEGREE_X)
        pan_dy = int((self.camera.CAMERA_CENTER_Y - pixel_y) / self.camera.PIXELS_PER_DEGREE_Y)
        self.gimbal.pan_goto(self.gimbal.x-pan_dx, self.gimbal.y-pan_dy)

    def stop_track(self):
        self.camera.stop_camera()
        self.gimbal.stop_gimbal()
        print("stop - Stopping")



#-----------------------------------------------------------------------------------------------
def face_track(gimbal, camera):
    if window_on:
        print("press q to quit opencv window display")
    else:
        print("press ctrl-c to quit SSH or terminal session")

    fps_counter = 0
    fps_start = time.time()

    # Initialize Timers for motion, face detect and pan/tilt search
    motion_start = time.time()
    face_start = time.time()
    pan_start = time.time()

    img_frame = camera.read()
    if WEBCAM:
        if (CAMERA_HFLIP and CAMERA_VFLIP):
            img_frame = cv.flip(img_frame, -1)
        elif CAMERA_HFLIP:
            img_frame = cv.flip(img_frame, 1)
        elif CAMERA_VFLIP:
            img_frame = cv.flip(img_frame, 0)
    
    grayimage1 = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY)
    print("===================================")
    print("Start Tracking Motion, Look for Faces when motion stops ....")
    print("")
    still_scanning = True
    while still_scanning:
        motion_found = False
        face_found = False
        Nav_LR = 0
        Nav_UD = 0
        if show_fps:
            fps_start, fps_counter = show_FPS(fps_start, fps_counter)
        img_frame = camera.read()
        if WEBCAM:
            if (CAMERA_HFLIP and CAMERA_VFLIP):
                img_frame = cv.flip(img_frame, -1)
            elif CAMERA_HFLIP:
                img_frame = cv.flip(img_frame, 1)
            elif CAMERA_VFLIP:
                img_frame = cv.flip(img_frame, 0)
        if check_timer(motion_start, timer_motion):  # Search for Motion and Track
            grayimage2 = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY)
            motion_center = motion_detect(grayimage1, grayimage2)
            grayimage1 = grayimage2  # Reset grayimage1 for next loop
            if motion_center != ():
                motion_found = True
                cx = motion_center[0]
                cy = motion_center[1]
                if debug:
                    print("face-track - Motion At cx={cx} cy={cy}")
                Nav_LR = int((cam_cx - cx) / 7)
                Nav_UD = int((cam_cy - cy) / 6)
                pan_cx = pan_cx - Nav_LR
                pan_cy = pan_cy - Nav_UD
                if debug:
                    print("face-track - Pan To pan_cx={pan_cx} pan_cy={pan_cy} Nav_LR={Nav_LR} Nav_UD={Nav_UD}")
                pan_goto(pan_cx, pan_cy)
                pan_cx, pan_cy = pan_goto(pan_cx, pan_cy)
                motion_start = time.time()
            else:
                face_start = time.time()
        elif check_timer(face_start, timer_face):
            # Search for Face if no motion detected for a specified time period
            face_data = face_detect(img_frame)
            if face_data != ():
                face_found = True
                (fx, fy, fw, fh) = face_data
                cx = int(fx + fw/2)
                cy = int(fy + fh/2)
                Nav_LR = int((cam_cx - cx) /7 )
                Nav_UD = int((cam_cy - cy) /6 )
                pan_cx = pan_cx - Nav_LR
                pan_cy = pan_cy - Nav_UD
                if debug:
                    print("face-track - Found Face at pan_cx={pan_cx} pan_cy={pan_cy} Nav_LR={Nav_LR} Nav_UD={Nav_UD}")
                pan_cx, pan_cy = pan_goto(pan_cx, pan_cy)
                face_start = time.time()
            else:
                pan_start = time.time()
        elif check_timer(pan_start, timer_pan):
            pan_cx, pan_cy = pan_search(pan_cx, pan_cy)
            pan_cx, pan_cy = pan_goto (pan_cx, pan_cy)
            img_frame = camera.read()
            if WEBCAM:
                if (CAMERA_HFLIP and CAMERA_VFLIP):
                    img_frame = cv.flip(img_frame, -1)
                elif CAMERA_HFLIP:
                    img_frame = cv.flip(img_frame, 1)
                elif CAMERA_VFLIP:
                    img_frame = cv.flip(img_frame, 0)
            grayimage1 = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY)
            pan_start = time.time()
            motion_start = time.time()
        else:
            motion_start = time.time()

        if window_on:
            if face_found:
                cv.rectangle(img_frame,(fx,fy), (fx+fw,fy+fh), blue, LINE_THICKNESS)
            if motion_found:
                cv.circle(img_frame, (cx,cy), CIRCLE_SIZE, green, LINE_THICKNESS)

            if WINDOW_BIGGER > 1:  # Note setting a bigger window will slow the FPS
                img_frame = cv.resize( img_frame,( big_w, big_h ))

            cv.imshow('Track q quits', img_frame)

            # Close Window if q pressed while movement status window selected
            if cv.waitKey(1) & 0xFF == ord('q'):
                camera.stop()
                cv.destroyAllWindows()
                print("face_track - End Motion Tracking")
                still_scanning = False

#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        face_tracker = FaceTracker()
        face_tracker.track_face()
    except KeyboardInterrupt:
        print("User Pressed Keyboard ctrl-c")
    finally:
        face_tracker.stop_track()
        print("Stopped Tracking")



