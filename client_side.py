import socket
import threading
import cv2
import pickle
import struct
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = 'localhost'  # Server IP address
video_port = 9000
chat_port = 9001


# Function to receive video frames from the server
def receive_video():
    try:
        while True:
            packet = client_socket.recv(4)
            if not packet:
                break
            msg_size = struct.unpack("I", packet)[0]
            data = b""
            while len(data) < msg_size:
                packet = client_socket.recv(4 * 1024)
                if not packet:
                    break
                data += packet
            frame_data = data
            frame = pickle.loads(frame_data)

            # Display the video frame from the server
            cv2.imshow("Video Stream", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    except Exception as e:
        print(f"Error receiving video: {str(e)}")


# Function to send chat messages to the server
def send_chat_message(event=None):
    message = chat_input.get()
    if message:
        chat_input.delete(0, tk.END)
        chat_message = f"CHAT:{message}"
        client_socket.send(chat_message.encode())


# Function to prompt the user for a username
def get_username():
    while True:
        try:
            username = simpledialog.askstring("Username", "Enter your username:")
            if username:
                return username
        except Exception as e:
            print(f"Error getting username: {str(e)}")


if __name__ == "__main__":
    # Connect to the video server
    client_socket.connect((host_ip, video_port))

    # Prompt the user for a username
    username = get_username()

    # Create the client's UI
    client_window = tk.Tk()
    client_window.title(f"Chat Room - {username}")

    # Create a chat box
    chat_box = scrolledtext.ScrolledText(client_window)
    chat_box.pack(padx=10, pady=10)

    # Create an input field for chat messages
    chat_input = tk.Entry(client_window)
    chat_input.pack(padx=10, pady=10)

    # Bind the Enter key to send chat messages
    chat_input.bind("<Return>", send_chat_message)

    # Create a send button to send chat messages
    send_button = tk.Button(client_window, text="Send", command=send_chat_message)
    send_button.pack(padx=10, pady=10)

    # Start receiving video frames from the server
    video_thread = threading.Thread(target=receive_video)
    video_thread.start()

    # Start the Tkinter main loop
    client_window.mainloop()
x
