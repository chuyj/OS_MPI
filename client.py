#! /usr/bin/env python3
import socket
import psutil

while True:
    per = psutil.cpu_percent(interval=0.25)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
    sock.connect(('192.168.0.201', 8889))
    msg = str(per) + '\n' 
    sock.send(msg.encode())
    data = sock.recv(5).decode()
    print(data)

