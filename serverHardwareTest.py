import time
import BaseHTTPServer
import json
import serial #Requires PySerial
import serial.tools.list_ports
import time
import urllib

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

def turnRight(value, T):
    idx = [3,[1,4],[2,5],6]
    for i in idx:
        if type(i) is not list:
            if i != 6:
                # print i
                SetVoicecoil(i, value)
                time.sleep(T/4.)
                SetVoicecoil(i, 0)
            else:
                # print i
                SetMotor(2, int(value/2.0))
                SetMotor(6, int(value/2.0))
                SetVoicecoil(i, value)
                time.sleep(T/2.)
                SetMotor(2, 0)
                SetMotor(6, 0)
                SetVoicecoil(i, 0)

        else:
            # print i
            SetVoicecoil(i[0], value)
            SetVoicecoil(i[1], value)
            time.sleep(T/4.)
            SetVoicecoil(i[0], 0)
            SetVoicecoil(i[1], 0)

def turnLeft(value, T):
    idx = [6,[2,5],[1,4],3]
    for i in idx:
        if type(i) is not list:
            if i != 3:
                # print i
                SetVoicecoil(i, value)
                time.sleep(T/4.)
                SetVoicecoil(i, 0)
            else:
                # print i
                SetMotor(1, int(value/2.0))
                SetMotor(5, int(value/2.0))
                SetVoicecoil(i, value)
                time.sleep(T/2.)
                SetMotor(1, 0)
                SetMotor(5, 0)
                SetVoicecoil(i, 0)

        else:
            # print i
            SetVoicecoil(i[0], value)
            SetVoicecoil(i[1], value)
            time.sleep(T/4.)
            SetVoicecoil(i[0], 0)
            SetVoicecoil(i[1], 0)

def drowsyAlert(value):
    idx = [1,2,5,6]
    for i in idx:
        SetMotor(i, int(value/2.0))
    
    time.sleep(0.1)
    
    for i in idx:
        SetMotor(i, 0)


def stopPad():
    for i in range(1,7):
        SetVoicecoil(i, 0)
        SetMotor(i, 0)

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
        
        query_components = parse_qs(urlparse(s.path).query)
        instrucion = urllib.unquote(query_components["instrucion"][0])
        ahead = int(query_components["ahead"][0])
        hapIntens = int(query_components["hapIntens"][0])

        # stopPad()
        if 'Drowsy' in instrucion:
            drowsyAlert(hapIntens)

        if 'left' in instrucion:
            
            if 'Turn' in instrucion:
                if ahead == 1:
                    turnLeft(int(hapIntens*0.75), 1)
                else:
                    for i in xrange(2):
                        turnLeft(hapIntens, 0.5)
                        time.sleep(0.5)
            else:
                if ahead == 0:
                    SetMotor(1, hapIntens)
                    SetMotor(5, hapIntens)
                    time.sleep(0.2)
                    SetMotor(1, 0)
                    SetMotor(5, 0)

        if 'right' in instrucion:
            
            if 'Turn' in instrucion:
                if ahead == 1:
                    turnRight(int(hapIntens*0.75), 1)
                else:
                    for i in xrange(2):
                        turnRight(hapIntens, 0.5)
                        time.sleep(0.5)
            else:
                if ahead == 0:
                    SetMotor(2, hapIntens)
                    SetMotor(6, hapIntens)
                    time.sleep(0.2)
                    SetMotor(2, 0)
                    SetMotor(6, 0)


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