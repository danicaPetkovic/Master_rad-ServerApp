import _thread
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO

from imutils import paths

import SaveImages

FTP_DIRECTORY = os.getcwd() + "\\downloads\\"


def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        print(body)

        imageList = list(SaveImages.IMAGES)
        images = []
        for i in range(len(imageList)):
            images.append(load_binary(FTP_DIRECTORY + imageList[i]))

        if body == b'Send image lenghts':
            count = ""
            for i in range(len(images)):
                count = count + str(len(images[i])) + ","
            count = count[:-1]
            count + "\n"
            print(count)
            response.write(count.encode())

        elif body == b'Send images':
            for i in range(len(images)):
                response.write(images[i])

        else:
            print("SaveImages.IMAGES")
            print(SaveImages.IMAGES)
            addedFiles = SaveImages.IMAGES
            data = str(body.decode('utf-8'))
            print(data)
            SaveImages.save_images(addedFiles, data)
            # SaveImages.aws_save_images(addedFiles, data)
            empty_download_folder()

        self.wfile.write(response.getvalue())


def start():
    print("HTTP Server started..")
    httpd = HTTPServer(('172.20.10.2', 49371), SimpleHTTPRequestHandler)
    # server.serve_forever()
    _thread.start_new_thread(httpd.serve_forever, tuple())


def empty_download_folder():
    imagePaths = list(paths.list_images(FTP_DIRECTORY))
    for image in imagePaths:
        os.remove(image)
