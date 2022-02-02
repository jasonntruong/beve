from imutils import paths
import face_recognition
import pickle
import cv2
import os
print(paths)
faceData = list(paths.list_images("/home/pi/beve/facesdataset"))
print(faceData)