import boto3
from imutils import paths
import os

AWS_DIRECTORY = os.getcwd() + "\\aws-microsoft-dataset\\"  # Fajl gde se nalazi image dataset
BUCKET = "security-sistem-aws"
COLLECTION = "aws-microsoft-dataset"


def train_model():
    imagePaths = list(paths.list_images(AWS_DIRECTORY))

    for path in imagePaths:
        name = os.path.splitext(os.path.basename(path))[0]
        add_faces_to_collection(path, name, COLLECTION)


def add_faces_to_collection(photo, person_name, collection_id):
    client = boto3.client('rekognition')
    imageSource = open(photo, 'rb')
    response = client.index_faces(CollectionId=collection_id,
                                  Image={'Bytes': imageSource.read()},
                                  ExternalImageId=person_name,
                                  MaxFaces=1,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['DEFAULT'])

    print('Results for ' + photo)
    print('Faces indexed:')
    for faceRecord in response['FaceRecords']:
        print('  External Image ID: ' + faceRecord['Face']['ExternalImageId'])
        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])