import _thread
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_PORT = 5000  # Port koji FTP server slusa, Mora da bude veci od 1023, osim ako se skripta run-uje kao root
FTP_USER = "call_server"  # FTP user za log in
FTP_PASSWORD = "serverMashine12!"  # FTP user password.

FTP_DIRECTORY = os.getcwd() + "\\downloads\\"  # Fajl gde ce FTP user da imam read/write pristup


def start():
    authorizer = DummyAuthorizer()

    # Definise se user sa full r/w permissions.
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')

    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "Reolink cliend connected."

    # Optionally specify range of ports to use for passive connections.
    # handler.passive_ports = range(60000, 65535)

    address = ('172.20.10.2', FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    print("FTP Server started..")
    # server.serve_forever()
    _thread.start_new_thread(server.serve_forever, tuple())

