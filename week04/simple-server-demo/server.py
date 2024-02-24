# python3 -m http.server

# from http.server import test, SimpleHTTPRequestHandler
#
# test(SimpleHTTPRequestHandler, port=8001)

#
from http.server import HTTPServer, SimpleHTTPRequestHandler

httpd = HTTPServer(('localhost', 8003), SimpleHTTPRequestHandler)
httpd.serve_forever()