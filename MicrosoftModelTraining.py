import os
import sys
import time

from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from imutils import paths
from msrest.authentication import CognitiveServicesCredentials

KEY = '620d5320d80c40e6acf2aaa2b9c95298'
ENDPOINT = 'https://master.cognitiveservices.azure.com/'

DATASET_DIRECTORY = os.getcwd() + "\\aws-microsoft-dataset\\"  # Fajl gde se nalazi image dataset
PERSON_GROUP_ID = 'microsoft-dataset'

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


# persons = face_client.person_group_person.list(PERSON_GROUP_ID)

def train_model():
    imagePaths = list(paths.list_images(DATASET_DIRECTORY))

    for path in imagePaths:
        print(path)
        name = os.path.splitext(os.path.basename(path))[0]
        print(name)

        person = face_client.person_group_person.create(PERSON_GROUP_ID, name)
        f = open(name + ".txt", "w")
        f.write(str(person))
        f.close()
        person = eval(open(name + '.txt', 'r').read())

        imageStream = open(path, 'r+b')
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, person["person_id"], imageStream)

    face_client.person_group.train(PERSON_GROUP_ID)

    while True:
        trainingStatus = face_client.person_group.get_training_status(PERSON_GROUP_ID)
        print("Training status: ", trainingStatus)
        if trainingStatus.status is TrainingStatusType.succeeded:
            break
        elif trainingStatus is TrainingStatusType.failed:
            sys.exit('Training the person group has failed.')
        time.sleep(5)