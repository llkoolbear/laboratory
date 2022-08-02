import cv2 as cv
from imutils.video import WebcamVideoStream
from imutils.video import FPS

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
fps = FPS().start()
while True:
    # Capture frame-by-frame
    grabbed, frame = cap.read()
    # if frame is read correctly ret is True
    if not grabbed:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

stream = WebcamVideoStream(0).start()
fps = FPS().start()

while not stream.stopped:
    # Capture frame-by-frame
    frame = stream.read()
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
    # Update the FPS counter
    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# When everything done, stop the stream
stream.stop()
cv.destroyAllWindows()