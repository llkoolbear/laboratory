import cv2 as cv
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils

# Load the cascade model
models_path = '/home/bearbissen/repos/opencv/data/haarcascades/'
frontal_face_model = models_path + 'haarcascade_frontalface_default.xml'
frontal_face_model_alt1 = models_path + 'haarcascade_frontalface_alt.xml'
frontal_face_model_alt2 = models_path + 'haarcascade_frontalface_alt2.xml'
profile_face_model = models_path + 'haarcascade_profileface.xml'
face = cv.CascadeClassifier(frontal_face_model)
profile = cv.CascadeClassifier(profile_face_model)
frontal_alt = cv.CascadeClassifier(frontal_face_model_alt1)
frontal_alt2 = cv.CascadeClassifier(frontal_face_model_alt2)



# Initialize Webcam and set properties
stream = WebcamVideoStream(0)
stream.stream.set(cv.CAP_PROP_FRAME_WIDTH, 640)
stream.stream.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
stream.stream.set(cv.CAP_PROP_FPS, 30)

# Initialize video stream
stream.start()
fps = FPS().start()

# To use a video file as input 
# cap = cv.VideoCapture('filename.mp4')

while not stream.stopped:
    # Read the frame
    frame = stream.read()
    frame = imutils.resize(frame, width=800)
    # if frame is read correctly ret is True
    # Convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face.detectMultiScale(gray, 1.1, 4)
    #frontal_alts = frontal_alt.detectMultiScale(gray, 1.1, 4)
    #frontal_alt2s = frontal_alt2.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each face
    if faces != ():
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    else:
        profiles = profile.detectMultiScale(gray, 1.1, 4)
        if profiles != ():
            for (x, y, w, h) in profiles:
                cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Display
    cv.imshow('img', frame)
    # Stop if escape key is pressed
    k = cv.waitKey(1) & 0xff
    if k==27:
        break
    # Update the FPS counter
    fps.update()
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Release the Stream
stream.stop()
cv.destroyAllWindows()
