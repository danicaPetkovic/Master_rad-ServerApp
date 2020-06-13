import os
import pickle
import face_recognition
from imutils import paths
import cv2

DATASET_DIRECTORY = os.getcwd() + "\\dataset\\train\\"   # Fajl gde se nalazi image dataset


def train_model():
    imagePaths = list(paths.list_images(DATASET_DIRECTORY))
    listKnownEncodings = []
    listKnownNames = []

    for (i, imagePath) in enumerate(imagePaths):
        print("obradjuje se slika {} od ukupno {}".format(i + 1, len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]

        # load the input image and convert it from BGR (OpenCV ordering) to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # vrsi se detekcija lica na slici. U okviru pravougaonka -boxes
        boxes = face_recognition.face_locations(rgb, model="hog")

        # svako lice nadjeno na slici se prevodi u 128bitni vektor
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            listKnownEncodings.append(encoding)
            listKnownNames.append(name)

    print("Serilizacija encodingsa..")
    data = {"encodings": listKnownEncodings, "names": listKnownNames}
    f = open("encodings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()