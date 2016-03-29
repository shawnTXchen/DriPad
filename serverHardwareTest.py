import time
import BaseHTTPServer
import json
import serial #Requires PySerial
import serial.tools.list_ports
import time

#Load Vybe device details
vybe_desc = {}
with open('vybe.json', 'r') as f:
    vybe_desc = json.load(f)


#Search for all connected Vybe devices
connectedDevices = []
for portcandidate in serial.tools.list_ports.comports():
    # print portcandidate[2]
    port_type = portcandidate[2] #each port description is a list of length 3; item 3 has vendor id and product id
    # if port_type.find('USB VID:PID=%s:%d'%(str(vybe_desc["comm"]["usbserial"]["vid"]), vybe_desc["comm"]["usbserial"]["pid"])) >= 0:
    if port_type.find('USB VID:PID=0483:5740')>= 0:
        print "Found %s"%(portcandidate[0],)
        connectedDevices.append(portcandidate[0]) #name of this port

#Connect to first found Vybe device
vybe = None
if connectedDevices:
    portname = connectedDevices[0]
    vybe = serial.Serial(port=portname, baudrate=vybe_desc["comm"]["usbserial"]["baud"], writeTimeout = 0.05)
else:
    raise IOError("%s not detected."%(vybe_desc["name"],))

#####################################
#
# Functions for activating actuators
#
#####################################

def SetVoicecoil(index, value):
    # Set value to [0,255]
    value = min(max(0, value), 255)

    # format: "VCL <number as character> <buzz value 0-255 as character\n"
    msg =   "VCL %s %s\n"%(str(index), chr(value))
    vybe.write(msg)
    vybe.flush()


def SetMotor(index, value):
    value = min(max(0, value), 255)

    # format: "MTR <number as character> <buzz value 0-255 as character\n"
    msg =   "MTR %s %s\n"%(str(index), chr(value))
    vybe.write(msg)
    vybe.flush()


#####################################
#
# Functions for server
#
#####################################


HOST_NAME = '127.0.0.1' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080 # Maybe set this to 9000.

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
        
        # print "---Path name: "
        # print s.path

        query_components = parse_qs(urlparse(s.path).query)
        
        # print "---Direction: "
        # print query_components["direction"][0]
        
        direction = query_components["direction"] 
        # name(direction[0])
        print "---direction:"
        print direction[0]

        if direction[0]=='Left':
            SetMotor(1, 255)
            time.sleep(2)
            SetMotor(1, 0)


        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        # s.wfile.write("<html><head><title>Title goes here.</title></head>")
        # s.wfile.write("<body><p>This is a page."+ direction[0] +"</p>")

        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".

        # s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        # s.wfile.write("</body></html>")

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