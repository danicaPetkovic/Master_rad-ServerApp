import datetime

import cv2
from firebase_admin import messaging, initialize_app, credentials, storage
import firebase_admin.messaging

registration_token = "efFGFfiHu2k:APA91bEILOlkk9BnrLkNhctXfXWlJvVIo3_11QE2VREcpBOZYpTZyI56ehagR8Ji_6uXw7iQSrA8pxtXn4ZfjDpWMS95pGDTRjDRmusd3rkYVkGLjQOhFEcXMvuHcKqbHwllIeMjwVG7"

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
firebase_admin.get_app()


def send_message():
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title='Uknown persons detected',
            body='Click to see unknown detected persons',
        ),
        token=registration_token
    )
    """
    message = messaging.Message(
        data={
            'title': 'Unknown persons detected',
            'body': 'Click to see unknown detected persons',
        },
        token=registration_token,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
