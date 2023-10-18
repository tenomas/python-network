import socket
import tkinter as tk
from threading import Thread

# Create a socket and connect to the chat server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('server_ip', 9000)  # Replace with your server's IP and port
client_socket.connect(server_address)

# Create the chat GUI
root = tk.Tk()
root.title("Chat Client")

message_listbox = tk.Listbox(root)
message_listbox.pack()

message_entry = tk.Entry(root)
message_entry.pack()

# Function to receive messages from the server
def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            message_listbox.insert(tk.END, message)
        except:
            # Handle errors or disconnections
            break

# Function to send messages to the server

root.mainloop()
