#  coding: utf-8
import socketserver
import os
import os.path
import mimetypes

# Copyright 2022 Abram Hindle, Eddie Antonio Santos, Jason Branch-Allen
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2022 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

''' 
CITATIONS

Ventura, J. (2020, November 22). Building a basic HTTP server from scratch in Python. Codementor. Retrieved January 24, 2022, from https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842 

learnpython.org, "String Formatting", https://www.learnpython.org/en/String_Formatting#:~:text=Python%20uses%20C%2Dstyle%20string,%22%20and%20%22%25d%22., Accessed On. January 24, 2022.

praavDa. (2009, June 3). Custom simple python HTTP server not serving CSS files. Stack Overflow. Retrieved January 28, 2022, from https://stackoverflow.com/questions/947372/custom-simple-python-http-server-not-serving-css-files. Answered by: nosklo(2009, June 3).

Howard, J. (2011, February 28). Find the current directory and file's directory. Stack Overflow. Retrieved January 28, 2022, from https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory. Answered By: Russell Dias(2011, February 28).

Documentation: Mozilla. (n.d.). 301 moved permanently - http: MDN. HTTP | MDN. Retrieved January 27, 2022, from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/301 

sharky. (2015, January 16). How do I setup a local HTTP server using Python. Stack Overflow. Retrieved January 24, 2022, from https://stackoverflow.com/questions/27977972/how-do-i-setup-a-local-http-server-using-python. Answered By: stvsmth(2015, January 15).

tparrott. (2010, July 20). BaseHTTPServer not recognizing CSS files. Stack Overflow. Retrieved January 25, 2022, from https://stackoverflow.com/questions/3291120/basehttpserver-not-recognizing-css-files. Answered By: John La Rooy(2010, July 20).

Bailey, C. (2019, July 7). How To Create a Simple Web Server Using Python and the http.server Module. YouTube. Retrieved January 26, 2022, from https://www.youtube.com/?gl=NL 

masroore. (2015, October 10). Typeerror: A bytes-like object is required, not 'str' when writing to a file in Python3. Stack Overflow. Retrieved January 25, 2022, from https://stackoverflow.com/questions/33054527/typeerror-a-bytes-like-object-is-required-not-str-when-writing-to-a-file-in. Answered By: Martijin Pieters(2015, October 10).

Os path module in python. GeeksforGeeks. (2020, November 29). Retrieved January 25, 2022, from https://www.geeksforgeeks.org/os-path-module-python/

Create a python web server. Create a Python Web Server - Python Tutorial. (n.d.). Retrieved January 24, 2022, from https://pythonbasics.org/webserver/ 

Python String isalpha() Method. W3Schools. (n.d.). Retrieved January 27, 2022, from https://www.w3schools.com/python/ref_string_isalpha.asp 

Python: Os.path.exists() method. GeeksforGeeks. (2019, May 21). Retrieved January 28, 2022, from https://www.geeksforgeeks.org/python-os-path-exists-method/ 

Bentley4. (2012, May 15). A simple website with python using simplehttpserver and SocketServer, how to only display the HTML file and not the whole directory? Stack Overflow. Retrieved January 28, 2022, from https://stackoverflow.com/questions/10607621/a-simple-website-with-python-using-simplehttpserver-and-socketserver-how-to-onl. Answered By: Susam Pal(2012, May 15).

Mimetypes - map filenames to mime types¶. mimetypes - Map filenames to MIME types - Python 3.10.2 documentation. (n.d.). Retrieved January 28, 2022, from https://docs.python.org/3/library/mimetypes.html 
'''


cwd = os.getcwd()
# firstPath = cwd / 'www' / 'index.html'


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        data = self.data.decode()
        http_header = data.split('\r\n')[0]
        file_path = http_header.split()[1]
        request_method = http_header.split()[0]
        extension = file_path.split('/')[-1]
        path_ending = file_path[-1]
        firstPath = './www' + file_path
        # print(data)
        # print(http_header)
        # print(http_command)

        # Handle HTTP requests
        if len(data) > 0:
            if request_method != 'GET':
                self.request.sendall(bytearray(
                    "HTTP/1.1 405 Method Not Allowed\r\n", 'utf-8'))
            elif os.path.exists(firstPath) and extension.isalpha():

                if os.path.isdir(firstPath):
                    self.request.sendall(
                        bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + file_path + '/' + "\r\n", 'utf-8'))
                else:
                    self.request.sendall(
                        bytearray("HTTP/1.1 404 NOT FOUND\r\nFile Not Found", 'utf-8'))
            else:
                self.server_requests(file_path)

        else:
            self.request.sendall(
                bytearray("HTTP/1.1 400 Bad Request\r\nBad Request", 'utf-8'))

        print("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray("OK\r\n", 'utf-8'))

    def server_requests(self, file_path):
        firstPath = './www' + file_path
        secondPath = './www' + file_path + '/index.html'
        path_ending = file_path[-1]
        extension = file_path.split('/')[-1]

        try:
            if os.path.realpath(cwd + '/www' + file_path).startswith(cwd + '/www'):
                if os.path.exists(secondPath) and file_path.endswith('/'):
                    fin = open(secondPath)
                    content = fin.read()
                    # print(content)
                    if content != None:
                        self.request.sendall(bytearray(
                            "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n" + content, 'utf-8'))
                    else:
                        self.request.sendall(
                            bytearray("HTTP/1.1 404 NOT FOUND\r\nFile Not Found", 'utf-8'))
                    fin.close()
                elif os.path.exists(firstPath) and (file_path.endswith('.html') or file_path.endswith('.css')):
                    mimetype, _ = mimetypes.guess_type(file_path)
                    fin = open("./www" + file_path)
                    content = fin.read()
                    # Check if the mimetype is either text/html or text/css
                    if mimetype == 'text/html':
                        self.request.sendall(bytearray(
                            "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n" + content, 'utf-8'))
                    elif mimetype == 'text/css':
                        self.request.sendall(bytearray(
                            "HTTP/1.1 200 OK\r\n" + "Content-Type: text/css\r\n" + content, 'utf-8'))
                    fin.close()
                else:
                    try:
                        fin = open(secondPath)
                        content = fin.read()
                        self.request.sendall(
                            bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + file_path + '/' + "\r\n", 'utf-8'))
                        fin.close()
                    except FileNotFoundError:
                        self.request.sendall(
                            bytearray("HTTP/1.1 404 NOT FOUND\r\nFile Not Found", 'utf-8'))

        except FileNotFoundError:
            self.request.sendall(
                bytearray("HTTP/1.1 404 NOT FOUND\r\nFile Not Found", 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    print("Server running on port %s" % PORT)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
