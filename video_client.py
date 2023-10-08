import socket
import cv2
import threading
import tkinter as tk
from tkinter import scrolledtext

from sympy.printing import numpy

# Create a Tkinter window for the chat
chat_window = tk.Tk()
chat_window.title("Chat")

# Create a scrolled text widget for displaying chat messages
chat_display = scrolledtext.ScrolledText(chat_window, height=10, width=50)
chat_display.pack()

# Create an entry widget for typing chat messages
chat_entry = tk.Entry(chat_window, width=50)
chat_entry.pack()

# Create a socket for video streaming
video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_host = 'localhost'
video_port = 9000

# Connect to the video server
video_socket.connect((video_host, video_port))

# Function to receive video frames and display them
def receive_video_frames():
    while True:
        try:
            frame_data = b""
            while True:
                packet = video_socket.recv(4096)
                if not packet:
                    break
                frame_data += packet
            if not frame_data:
                continue

            # Deserialize the frame
            frame = cv2.imdecode(numpy.frombuffer(frame_data, dtype=numpy.uint8), 1)

            # Display the video frame (you may need to create a separate window)
            cv2.imshow("Video", frame)
            cv2.waitKey(1)

        except Exception as e:
            # Handle any socket errors or server disconnections here
            print(f"Video Server disconnected: {e}")
            break

# Create a thread to continuously receive video frames
video_receive_thread = threading.Thread(target=receive_video_frames)
video_receive_thread.daemon = True
video_receive_thread.start()

# Create a socket for chat
chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_host = 'localhost'
chat_port = 9001

# Connect to the chat server
chat_socket.connect((chat_host, chat_port))

# Function to send chat message to the server
def send_chat_message():
    message = chat_entry.get()
    chat_entry.delete(0, tk.END)  # Clear the entry field after sending
    chat_message = f"CHAT:{message}"
    chat_socket.send(chat_message.encode())

# Function to display chat messages in the GUI
def display_chat_message(message):
    chat_display.insert(tk.END, message + '\n')
    chat_display.see(tk.END)  # Scroll to the bottom to show the latest message

# Function to continuously receive and display chat messages
def receive_chat_messages():
    while True:
        try:
            chat_message = chat_socket.recv(1024).decode()
            if chat_message.startswith("CHAT:"):
                chat_message = chat_message[5:]  # Remove "CHAT:" prefix
                display_chat_message(chat_message)
        except Exception as e:
            # Handle any socket errors or server disconnections here
            print(f"Chat Server disconnected: {e}")
            break

# Create a thread to continuously receive chat messages
chat_receive_thread = threading.Thread(target=receive_chat_messages)
chat_receive_thread.daemon = True
chat_receive_thread.start()

# Bind the Enter key to send chat messages
chat_entry.bind("<Return>", lambda event: send_chat_message())

# Start the Tkinter main loop
chat_window.mainloop()
