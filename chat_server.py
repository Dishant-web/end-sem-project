import socket
import threading
import json
from datetime import datetime

class ChatServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server started on {self.host}:{self.port}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            thread.start()
            
    def handle_client(self, client_socket, address):
        # Get username
        try:
            username = json.loads(client_socket.recv(1024).decode())['username']
            self.clients[client_socket] = username
            
            self.broadcast(f"{username} joined the chat!")
            
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                    
                data = json.loads(message)
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted_message = f"[{timestamp}] {username}: {data['message']}"
                self.broadcast(formatted_message, exclude=client_socket)
                
        except:
            pass
        finally:
            if client_socket in self.clients:
                username = self.clients[client_socket]
                del self.clients[client_socket]
                self.broadcast(f"{username} left the chat!")
            client_socket.close()
            
    def broadcast(self, message, exclude=None):
        for client in self.clients:
            if client != exclude:
                try:
                    client.send(json.dumps({"message": message}).encode())
                except:
                    continue
                    
if __name__ == "__main__":
    server = ChatServer()
    server.start()