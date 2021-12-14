#encoding: utf-8

import os
import sys
import socket
import select


def main():
    server = socket.socket()
    server.bind(('127.0.0.1', 50051))
    server.listen(5)
    print('start server on 127.0.0.1 listen port 50051 ...')
    while True:
        conn, addr = server.accept()
        print(conn, addr)
        while True:
            data = conn.recv(1024)
            print(data)
            if not data:
                print('recv complete')
                break
            conn.send(data.upper())
    server.close()


if __name__ == '__main__':
    main()
