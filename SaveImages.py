import os
import uuid
import cv2
from imutils import paths

import AmazonModelTraining
import FTPClient
import FaceNetModelTraining
import FaceRecognitionModelTraining
import MicrosoftModelTraining

DOWNLOADS = os.getcwd() + "\\downloads\\"
DATASET_DIRECTORY = os.getcwd() + "\\dataset\\train\\"  # Fajl gde se nalazi image dataset
AWS_DIRECTORY = os.getcwd() + "\\aws-microsoft-dataset\\"  # Fajl gde se nalazi image dataset
IMAGES = []
image_count = 5


def save_images(saveImages, names):
    images = list(saveImages)
    print(images)
    print(names)
    nameList = names.split(',')
    if len(images) != len(nameList):
        return False  # imamo vise slika nego imena, a treba nam isti broj (mapiranja)

    dirs = dict([(f, None) for f in os.listdir(DATASET_DIRECTORY)])

    for i in range(len(nameList)):
        name = nameList[i].lower().replace(' ', '_')
        if name == 'unknown':
            continue
        if name in dirs:
            image = cv2.imread(DOWNLOADS + images[i])
            cv2.imwrite(DATASET_DIRECTORY + name + '\\' + uuid.uuid4().hex + '.jpg', image)
            os.remove(DOWNLOADS + images[i])
        else:
            image = cv2.imread(DOWNLOADS + images[i])
            os.mkdir(DATASET_DIRECTORY + name)
            cv2.imwrite(DATASET_DIRECTORY + name + '\\' + uuid.uuid4().hex + '.jpg', image)
            os.remove(DOWNLOADS + images[i])

    if len(os.listdir(DATASET_DIRECTORY)) - image_count > 3:
        train_models()
    return True


def aws_save_images(saveImages, names):
    images = list(saveImages)
    nameList = names.split(',')
    if len(images) != len(nameList):
        return False  # imamo vise slika nego imena, a treba nam isti broj (mapiranja)

    dirs = dict([(f, None) for f in os.listdir(AWS_DIRECTORY)])

    for i in range(len(nameList)):
        name = nameList[i].lower().replace(' ', '_')
        if name == 'unknown':
            continue
        print(AWS_DIRECTORY + name + '.jpg')
        image = cv2.imread(DOWNLOADS + images[i])
        cv2.imwrite(AWS_DIRECTORY + name + '.jpg', image)
        os.remove(DOWNLOADS + images[i])

    if len(os.listdir(AWS_DIRECTORY)) > 3:
        train_cloud_models()
    return True


def get_images():
    for name in os.listdir(DATASET_DIRECTORY):
        print(name)
        for image in os.listdir(DATASET_DIRECTORY + name + '\\'):
            print(image)


def train_models():
    FaceNetModelTraining.train_model()
    FaceRecognitionModelTraining.train_model()

    files = ['encodings.pickle', 'dataset.npz', 'dataset-embeddings.npz']
    FTPClient.send_data_to_server(files)


def train_cloud_models():
    MicrosoftModelTraining.train_model()
    AmazonModelTraining.train_model()
    empty_aws_folder()


def empty_aws_folder():
    imagePaths = list(paths.list_images(AWS_DIRECTORY))
    for image in imagePaths:
        os.remove(image)


#train_models()
# save_images({'800.jpeg': None, '9223371931753044421.jpg': None, '9223371931753044432.jpg': None, 'lala.jpg': None}, 'shakira,beyonce,unknown,danica petkovic')