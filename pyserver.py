#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
import time
import threading
import glob
import os

class WebRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
#    def __init__(self, request, client_address, server, path_photos):
#	self.path_photos = path_photos
#    	SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
    path_photos = "html/fotos/"
	
    def list_photos(self):
	self.send_response(200)
	self.send_header('Content-type', 'application/json')
	self.end_headers()

	files = filter(os.path.isfile, glob.glob(WebRequestHandler.path_photos + "*.jpg"))
	files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
	self.wfile.write('{"photos":[\n')
	length = len(files)
	counter = 1
	for file in files:
	    filedate = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(os.path.getmtime(file)))
	    self.wfile.write('{"path":"/' + file + '", "date":"' + filedate  + '"}')
	    if counter < length:
		self.wfile.write(',')
	    self.wfile.write('\n')
	    counter = counter + 1

	self.wfile.write(']}\n')
	return

    def do_GET(self):
        if self.path == '/listphotos.js':
	    self.list_photos()
	    return
	elif self.path.startswith("/html/") == False:
	    self.path = "/html" + self.path

        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


