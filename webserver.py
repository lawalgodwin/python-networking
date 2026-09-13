#!/usr/bin/env python3

import socket
import sys

sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_ip = socket.gethostbyname(socket.gethostname())
server_port = int (sys.argv[1]) or 20123
SERVER_ADDR = ('', server_port)

sock_fd.bind(SERVER_ADDR)

sock_fd.listen()

def accept_request(sock):
    client, old_sock = sock.accept()
    handle_request(client)
    sock.close()

def handle_request(client):
    response_body = ""
    req = b""
    print(client)
    res = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/html\r\n"
            b"Connection: close\r\n"
            b"\r\n"
            b"<h1>Hello from socket server<h1>\r\n"
            b"\r\n"
    )
    while b"\r\n\r\n" not in req:
        data = client.recv(1024)
        if not data:
            print("all done")
            break
        req += data
    print(response_body)
    # send response back to client
    client.sendall(res)
    client.close()

print(f"[SERVER] is listen on {server_ip}:{20123}")

while True:
    # accept request from a client
    client, sock = sock_fd.accept()
    # handle request for client
    handle_request(client)
    print(sock)
