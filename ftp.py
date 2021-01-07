# Made with documentation: 
# https://pyftpdlib.readthedocs.io/en/latest/tutorial.html#a-base-ftp-server

import os
import logging
import socket

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 53))  # connecting to a UDP address doesn't send packets
ip = s.getsockname()[0]


def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user('root', 'toor', '.', perm='elradfmwMT')
    authorizer.add_user('raul', 'wierzba', './wierzba', perm='elradfmwMT')

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Storage log's in file
    logging.basicConfig(filename='./logs.log', level=logging.INFO)

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = (ip, 5051)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    print(f"[+] FTP Server has started on {ip}:{address[1]}")

    # start ftp server
    server.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except:
        print("[-] FTP Server has crashed")
