import imutils
import face_recognition
import pickle
import cv2
import os
import time
import np

def getFace(allVals):
    mostSimilar = 0
    mostSimilarFace = 0
    first = True
    whoMsg = ""

    #load encodings file from makeEncodings.py (holds encodings from dataset)
    faceData = pickle.loads(open('/home/pi/beve/FaceRecognition/encodings', 'rb').read())

    #image to find a face in
    imageToDetect = cv2.imread('/home/pi/beve/FaceRecognition/imageToDetect.png')   #user given face will be downloaded here
    print("image found")

    rgb =cv2.cvtColor(imageToDetect, cv2.COLOR_BGR2RGB)
    faceEncodings = face_recognition.face_encodings(rgb)

    #no face found in imageToDetect
    if len(faceEncodings) == 0:
        return "I see **no face**"

    for encoding in faceEncodings:
        faceMatches = face_recognition.compare_faces(faceData["encodings"], encoding) #boolean array of face matches

        #if user wants all user distances/values
        if allVals == True:
            whoMsg = "Here's **what I** see: "
            for i in range(len(faceMatches)):
                distance = np.linalg.norm(encoding - faceData["encodings"][i])
                percentMatch = (1 - distance)*100
                whoMsg += "\n" + faceData["names"][i] + ": " + str(percentMatch.round(2)) + "% match!"
        
        #if there is a match between dataset faces and the user given face
        elif True in faceMatches:
            whoMsg = "I **definitely** see: "
            for i in range(len(faceMatches)):
                if faceMatches[i] == True:
                    whoMsg += faceData["names"][i] + ", "
            whoMsg = whoMsg[:-2]
        
        #if no match and user doesn't want all values, print the closest face amongst the dataset
        elif allVals == False:
            print("F")
            whoMsg = "I **think I** see: "
            for i in range(len(faceMatches)):
                distance = np.linalg.norm(encoding - faceData["encodings"][i])

                if distance < mostSimilar or first == True:
                    first = False
                    mostSimilarFace = i
                    mostSimilar = distance

            first = True
            print(mostSimilar, mostSimilarFace)
            whoMsg += faceData["names"][mostSimilarFace]

    return whoMsg

if __name__ == "__main__":
    print(getFace(True))
    print(getFace(False))