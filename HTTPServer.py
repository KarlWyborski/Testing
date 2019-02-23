from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import time

class Serv(BaseHTTPRequestHandler):
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        self._set_headers()
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = 'File not found'
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
         
    def do_POST(self):
        print('I got a post request')
        content_len = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_len)
        print(str(body) + ' hgasdhfkj')
##        response.write(b'This is a POST request. ')
##        response.write(b'Recieved: ')
##        response.write(body)
        self._set_headers()
        self.wfile.write(body)



def startup():
    dataPath = './data'
    
    year = str(time.localtime()[0])
    
    if time.localtime()[1] < 10:
        month = '0' + str(time.localtime()[1])
    else:
        month = str(time.localtime()[1])
        
    if time.localtime()[2] < 10:
        day = '0' + str(time.localtime()[2])
    else:
        day = str(time.localtime()[2])
        
    
                        
    fileName = year + '_' + month + '_' + day + '.txt'
    if not os.path.isdir(dataPath):
        os.mkdir(dataPath)
        print('Creating ./data folder...')
        
    try:
        f = open(dataPath + '/' + fileName, 'r')
        print('File for today was found.')
    except FileNotFoundError:
        print('File for today not found. Creating new file...')
        f = open(dataPath + '/' + fileName, 'w')
        f.write('15')
        stamp = time.localtime()
        for i in stamp:
            f.write(',' + str(i))
    
    f.close()
        
def adjustTime(self):
        hourOffset = 0
        minOffset = 5
        secOffset = 30
        inTime = [0,0,0,0,0,0,0,0,0]
        i = 0
        while i < 9:
            inTime[i] = time.localtime()[i]
            i += 1
        
        if (inTime[5] + secOffset) > 59:
            minOffset += 1
            inTime[5] = inTime[5] + secOffset - 60
        elif (inTime[5] + secOffset) < 0:
            minOffset -= 1
            inTime[5] = inTime[5] + secOffset + 60
        else:
            inTime[5] = inTime[5] + secOffset
        
        if (inTime[4] + minOffset) > 59:
            hourOffset += 1
            inTime[4] = inTime[4] + minOffset - 60
        elif (inTime[4] + minOffset) < 0:
            hourOffset -= 1
            inTime[4] = inTime[4] + minOffset + 60
        else:
            inTime[4] = inTime[4] + minOffset
        
        inTime[3] = inTime[3] + hourOffset
        return inTime
    

##---------------------------

startup()
httpd = HTTPServer(('',8080), Serv)
httpd.serve_forever()
