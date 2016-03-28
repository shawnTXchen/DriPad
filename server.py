import time
import BaseHTTPServer


HOST_NAME = '127.0.0.1' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 4747 # Maybe set this to 9000.

def name(st):
    print st


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPServer.BaseHTTPRequestHandler.end_headers(self)
    def do_GET(s):
        from urlparse import urlparse, parse_qs
        print s.path

        query_components = parse_qs(urlparse(s.path).query)
        print query_components
        direction = query_components["direction"] 
        name(direction[0])
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a page."+ direction[0] +"</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)