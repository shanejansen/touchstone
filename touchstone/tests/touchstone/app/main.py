import http.server
import socketserver

handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(('', 8080), handler) as httpd:
    print('HTTP available on port 8080.')
    httpd.serve_forever()
