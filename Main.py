import os
import time

import FTPServer
import FirebaseMessaging
import HttpServer
import SaveImages

FTP_DIRECTORY = os.getcwd() + "\\downloads\\"  # Fajl gde ce FTP user da imam read/write pristup

registration_token = "efFGFfiHu2k:APA91bEILOlkk9BnrLkNhctXfXWlJvVIo3_11QE2VREcpBOZYpTZyI56ehagR8Ji_6uXw7iQSrA8pxtXn4ZfjDpWMS95pGDTRjDRmusd3rkYVkGLjQOhFEcXMvuHcKqbHwllIeMjwVG7"


def main():
    FTPServer.start()
    HttpServer.start()

    # file watcher
    beforeFiles = dict([(f, None) for f in os.listdir(FTP_DIRECTORY)])
    while True:
        time.sleep(10)
        afterFiles = dict([(f, None) for f in os.listdir(FTP_DIRECTORY)])
        addedFiles = [f for f in afterFiles if not f in beforeFiles]
        removedFiles = [f for f in beforeFiles if not f in afterFiles]
        if addedFiles: print("Added: ", ", ".join(addedFiles))
        if removedFiles: print("Removed: ", ", ".join(removedFiles))
        beforeFiles = afterFiles

        if addedFiles:
            # data = SocketClient.send_to_android(addedFiles)
            FirebaseMessaging.send_message()
            SaveImages.IMAGES = afterFiles


if __name__ == "__main__":
    main()