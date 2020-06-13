import os
from os import listdir
from os.path import isdir
from PIL import Image
from numpy import asarray, savez_compressed, expand_dims, load
from mtcnn.mtcnn import MTCNN
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder, Normalizer
from sklearn.svm import SVC

DATASET_DIRECTORY = os.getcwd() + "\\dataset\\"  # Fajl gde se nalazi image dataset


# load a dataset that contains one subdir for each class that in turn contains images
def load_dataset(directory):
    faceList, nameList = list(), list()
    # enumerate folders, on per class
    for subdir in listdir(directory):
        # path
        path = directory + subdir + '/'
        # skip any files that might be in the dir
        if not isdir(path):
            continue
        # load all faces in the subdirectory
        faces = load_faces(path)
        # create labels
        labels = [subdir for _ in range(len(faces))]
        # summarize progress
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        # store
        faceList.extend(faces)
        nameList.extend(labels)
    return asarray(faceList), asarray(nameList)


# load images and extract faces for all images in a directory
def load_faces(directory):
    faces = list()
    # enumerate files
    for filename in listdir(directory):
        # path
        path = directory + filename
        # get face
        faceList = extract_faces(path)
        # store
        faces.append(faceList)
    return faces


def extract_faces(filename, required_size=(160, 160)):
    image = Image.open(filename)
    image = image.convert('RGB')
    pixels = asarray(image)
    detector = MTCNN()
    results = detector.detect_faces(pixels)
    x1, y1, width, height = results[0]['box']
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = pixels[y1:y2, x1:x2]
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array


def load_trainTest_dataset(trainDirectory, testDirectory):
    # load train dataset
    trainX, trainy = load_dataset(trainDirectory)
    print(trainX.shape, trainy.shape)
    # load test dataset
    testX, testy = load_dataset(testDirectory)
    print(testX.shape, testy.shape)
    # save arrays to one file in compressed format
    savez_compressed('dataset.npz', trainX, trainy, testX, testy, allow_pickle=True)


# create embeddings
# datasetNPZ = 'dataset.npz'
def create_model_embeddings(datasetNPZ):
    # load the face dataset
    data = load(datasetNPZ)
    data.allow_pickle = True
    trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    print('Loaded: ', trainX.shape, trainy.shape, testX.shape, testy.shape)
    # load the facenet model
    model = load_model('facenet_keras.h5')
    print('Loaded Model')
    """
    # convert each face in the train set to an embedding
    newTrainX = list()
    for face_pixels in trainX:
        embedding = get_embedding(model, face_pixels)
        newTrainX.append(embedding)
    newTrainX = asarray(newTrainX)
    print(newTrainX.shape)
    # convert each face in the test set to an embedding
    newTestX = list()
    for face_pixels in testX:
        embedding = get_embedding(model, face_pixels)
        newTestX.append(embedding)
    newTestX = asarray(newTestX)
    print(newTestX.shape)
    # save arrays to one file in compressed format
    savez_compressed('dataset-embeddings.npz', newTrainX, trainy, newTestX, testy)
    """
    newTrainX = []
    for face_pixels in trainX:
        embedding = get_embedding(model, face_pixels)
        newTrainX.append(embedding)
    newTrainX = asarray(newTrainX)
    print(newTrainX.shape)
    # convert each face in the test set to an embedding
    newTestX = []
    for face_pixels in testX:
        embedding = get_embedding(model, face_pixels)
        newTestX.append(embedding)
    newTestX = asarray(newTestX)
    print(newTestX.shape)
    # save arrays to one file in compressed format
    savez_compressed('dataset-embeddings.npz', newTrainX, trainy, newTestX, testy)


# get the face embedding for one face
def get_embedding(model, face_pixels):
    # scale pixel values
    face_pixels = face_pixels.astype('float32')
    # standardize pixel values across channels (global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    # transform face into one sample
    samples = expand_dims(face_pixels, axis=0)
    # make prediction to get embedding
    yhat = model.predict(samples)
    return yhat[0]


def train_model():
    load_trainTest_dataset(DATASET_DIRECTORY + "\\train\\", DATASET_DIRECTORY + "\\val\\")
    create_model_embeddings('dataset.npz')


def get_embeddings(face_pixels):
    model = load_model('facenet_keras.h5')
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = expand_dims(face_pixels, axis=0)
    embedding = model.predict(samples)
    return embedding[0]
