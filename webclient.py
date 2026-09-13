#!/usr/bin/env python3

import sys 

import socket

SERVER_IP = socket.gethostbyname(sys.argv[1]) if sys.argv[1] else socket.gethostbyname(socket.gethostname)
PORT = int(sys.argv[2]) or 80
ADDR = (SERVER_IP, PORT)
print(f"[ADDRESS] {ADDR[0]}:{ADDR[1]}")

soc_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_fd.connect(ADDR)
req = (
    b"GET / HTTP/1.1\r\n" + 
    f"Host: {sys.argv[1]}\r\n".encode("ISO-8859-1") + 
    b"Connection: close\r\n"
    b"\r\n"
    b"Hello from socket client\r\n"
    b"\r\n"
)
soc_fd.sendall(req)

# print("--------RESPONSE HERDER--------")
body = ""
while True:
    data = soc_fd.recv(1024)
    if not data:
        break
    body += data.decode("ISO-8859-1")

# print("--------RESPONSE BODY--------")
print(body)
soc_fd.close()
