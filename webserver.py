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
    request = b""
    headers_delimiter = b"\r\n\r\n"
    res = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/html\r\n"
            b"Connection: close\r\n"
            b"\r\n"
            b"<h1>Hello from socket server<h1>\r\n"
            b"\r\n"
    )
    while headers_delimiter not in request:
        request = client.recv(1024)

    # Get the request headers (request = headers + body)
    request_headers_bytes, body = request.split(headers_delimiter, 1)
    content_length = 0

    for line in request_headers_bytes.decode("ISO-8859-1").splitlines():
        print(line)
        if line.startswith("Content-Length:"):
            content_length = int(line.split(":")[1].strip())
    print()
    print("done reading all request headers")
    print("\nReading the request body\n")
    # Get the request body if there is any
    while len(body) < content_length:
        body += client.recv(1024)
    print(body.decode("ISO-8859-1"))
    print("\nDone reading the request body")
    # send response back to client
    client.sendall(res)
    client.close()

print(f"[SERVER] is listen on {server_ip}:{20123}")

while True:
    # accept request from a client
    client, sock = sock_fd.accept()
    print(f"[SERVER] accepted connection from {client.getpeername()[0]}:{client.getpeername()[1]}")
    # handle request for client
    handle_request(client)
