#only ran when face dataset is altered (updates the encodings file)

from imutils import paths
import face_recognition
import pickle
import cv2
import os

facePaths = list(paths.list_images("/home/pi/beve/FaceRecognition/facesdataset"))
faceEncodings = []
names = []

for facePath in facePaths:
    name = facePath.split(os.path.sep)[-2] #gets name from the path
    image = cv2.imread(facePath)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #dlib ordering in RGB so change it
    boxes = face_recognition.face_locations(rgb, model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes) #face encodings that determine faces

    #append data to respective arrays
    for encoding in encodings:
        faceEncodings.append(encoding)
        names.append(name)

#add to dictionary and store it in an encodings file
data = {"encodings": faceEncodings, "names": names}

f = open("/home/pi/beve/FaceRecognition/encodings", "wb")
f.write(pickle.dumps(data))
f.close()

print(data)