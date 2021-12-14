#encoding: utf-8

import os
import sys
import time
import socket
import select


def main():
    client = socket.socket()
    client.connect(('127.0.0.1', 50051))

    while True:
        msg = input(">>:").strip()
        client.send(msg.encode())
        data = client.recv(1024)
        print('recv data:', data.decode())
    client.close()


if __name__ == '__main__':
    main()
