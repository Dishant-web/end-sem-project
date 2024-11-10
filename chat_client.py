import socket
import threading
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatClient:
    def __init__(self, host='localhost', port=5000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        
    def start(self):
        try:
            self.socket.connect((self.host, self.port))
            self.create_gui()
        except Exception as e:
            print(f"Couldn't connect to server: {e}")
            exit(1)
            
    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("Python Chat")
        self.window.geometry("600x400")
        
        # Username frame
        username_frame = tk.Frame(self.window)
        username_frame.pack(pady=10)
        
        tk.Label(username_frame, text="Username: ").pack(side=tk.LEFT)
        self.username_entry = tk.Entry(username_frame)
        self.username_entry.pack(side=tk.LEFT)
        tk.Button(username_frame, text="Join", command=self.join_chat).pack(side=tk.LEFT, padx=5)
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=50, height=20)
        self.chat_area.pack(padx=10, pady=5)
        self.chat_area.config(state=tk.DISABLED)
        
        # Message frame
        message_frame = tk.Frame(self.window)
        message_frame.pack(pady=10)
        
        self.message_entry = tk.Entry(message_frame, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=5)
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        tk.Button(message_frame, text="Send", command=self.send_message).pack(side=tk.LEFT)
        
        # Start receiving messages
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        
        self.window.mainloop()
        
    def join_chat(self):
        username = self.username_entry.get().strip()
        if username:
            self.username = username
            self.socket.send(json.dumps({"username": username}).encode())
            self.username_entry.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Please enter a username")
            
    def send_message(self):
        message = self.message_entry.get().strip()
        if message and hasattr(self, 'username'):
            self.socket.send(json.dumps({"message": message}).encode())
            self.message_entry.delete(0, tk.END)
        elif not hasattr(self, 'username'):
            messagebox.showerror("Error", "Please join the chat first")
            
    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()
                if message:
                    data = json.loads(message)
                    self.chat_area.config(state=tk.NORMAL)
                    self.chat_area.insert(tk.END, data['message'] + '\n')
                    self.chat_area.config(state=tk.DISABLED)
                    self.chat_area.see(tk.END)
            except:
                break
                
if __name__ == "__main__":
    client = ChatClient()
    client.start()