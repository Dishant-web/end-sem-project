from http.server import HTTPServer
from server.http_server import ChatHandler

def main():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, ChatHandler)
    print('Server running on port 3000...')
    httpd.serve_forever()

if __name__ == '__main__':
    main()