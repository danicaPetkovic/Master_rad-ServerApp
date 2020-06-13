import os
from ftplib import FTP_TLS, FTP

import cv2
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_PORT = 2121
FTP_USER = "reolinkE1"
FTP_PASSWORD = "reolink.123!"


def send_data_to_server(file_list):
    print(file_list)
    connection_status = True
    try:
        ftp = FTP()
        ftp.connect('172.20.10.2', FTP_PORT)
        ftp.login(FTP_USER, FTP_PASSWORD)
        print(ftp.getwelcome())

        for file_name in file_list:
            with open(file_name, 'rb') as file:
                ftp.storbinary('STOR ' + file_name, file)
            os.remove(file_name)
    except:
        connection_status = False

    return connection_status
