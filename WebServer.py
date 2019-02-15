import http.server
import socketserver

##PORT = 8080
Handler = http.server.BaseHTTPRequestHandler

class S(Handler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        self._set_headers()
        self.wfile.write(b"<html><body><h1>Hi!</h1></body></html>")
    
    def do_HEAD(self):
        self._set_headers()
    
    def do_POST(self):
        self._set_headers()
        self.wfile.write(b"<html><body><h1>POST!</h1></body></html>")

def run(server_class=http.server.HTTPServer, handler_class=S, PORT = 8080):
    server_address = ('',PORT)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == '__main__':
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()


##    
##print("serving at port", PORT)
##socketserver.TCPServer(("",PORT), Handler).serve_forever()
