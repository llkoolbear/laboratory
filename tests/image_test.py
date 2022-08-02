
import cv2 as cv
import sys

img_path = '/mnt/c/Users/bearb/Pictures/2017-07/IMG_20170713_121426.jpg'
img = cv.imread(cv.samples.findFile(img_path))
if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Display window", img)
k = cv.waitKey(10000)
if k == ord("s"):
    cv.imwrite("dad_bear_colorado.png", img)