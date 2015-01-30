#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle, Ana Marcu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriatel
import urllib
from urlparse import urlparse


def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    # def get_host_port(self,url):
    
    def parse_url(self, url):
        parsed_url = urlparse(url)
        
        
        try:
            host, port = parsed_url.netloc.split(":")
        except:
            host = parsed_url.netloc
            port = 80

        return host, int(port), parsed_url.path
    
    # connect to socket for host/port
    def connect(self, host, port):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sock.connect((host, port))
        
        return sock
    
    # retrieve http response code from the get/post return data
    def get_code(self, data):
        
        parsed_data = data.split()
        code = int(parsed_data[1])
        
        return code


    def get_headers(self,data):
        return None

    # retrieve the body from the get/post http response data
    def get_body(self, data):
        
        body = data.split("\r\n\r\n")
        body = body[-1]

        return body

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    # send get request to given url via socket, retrieve the response code and the body
    def GET(self, url, args=None):
        code = 500
        body = ""
    
  
        host, port, path = self.parse_url(url)

        sock = self.connect(host, int(port))

        sock.send("GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, str(host)))

        data = self.recvall(sock)
        
        code = self.get_code(data)
        
        body = self.get_body(data)

        sock.close()
        
        
        return HTTPRequest(code, body)
    
    # send post request to given url with the given arguments, retrieve the response code and the body(returned paramaters)
    def POST(self, url, args=None):
        code = 500
        body = ""
        
        host, port, path = self.parse_url(url)
        
        sock = self.connect(host, int(port))

        if args!=None:
            post_args = urllib.urlencode(args)
            length = len(post_args)
            post_args="\r\n"+post_args+"\r\n\r\n"
        else:
            post_args = "\r\n"
            length = 0

        sock.send("POST %s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: %s\r\n%s" % (path, str(host), str(length), post_args))
        
        data = self.recvall(sock)

        code = self.get_code(data)
        
        body = self.get_body(data)

        sock.close()


        return HTTPRequest(code, body)

    # call either the ge tor the post function
    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
