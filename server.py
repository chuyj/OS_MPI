#! /usr/bin/env python3
import os
import time
import json
import libvirt
import tornado.web
import tornado.gen
import tornado.ioloop
import tornado.process
from tornado import tcpserver
from pprint import pprint

title =  [['Time', 'Master', 'Slave1', 'Slave2']]
infolist = [[None]*10]
info = 	 [0,0,0,0]
map = {'192.168.0.201' : 1, '192.168.0.202' : 2, '192.168.0.203' : 3}

class TcpConnection(object):
    def __init__(self, stream, address):
        self.stream = stream
        self.address = address
        self.stream.read_until(b'\n', self.on_read_line)
        #print("new connection", address, stream)

    def on_read_line(self, data):
        data = data.decode()
        self.stream.write(data.encode())
        info[map[self.address[0]]] = float(data.rstrip())


class TCPServer(tornado.tcpserver.TCPServer):
       def handle_stream(self, stream, address):
           TcpConnection(stream, address)

class LoadHandler(tornado.web.RequestHandler):
    def get(self):
        global title, infolist
        pprint(title + infolist)
        self.write({"results":title + infolist})
        

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./template/index.html")

def make_app():
    return tornado.web.Application(
                debug=True,
                handlers=[(r"/", MainHandler),
                          (r"/loading", LoadHandler),],
           )
def tick():
    global infolist
    global info
    if len(infolist) > 10:
        infolist.pop(0)
    infolist.append(info.copy())
    for idx, _ in enumerate(infolist):
        infolist[idx][0] = idx - 10
    #print (infolist)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    server = TCPServer()
    server.listen(8889)
    tornado.ioloop.PeriodicCallback(tick, 1000).start();
    tornado.ioloop.IOLoop.current().start()
