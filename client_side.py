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
payload_size = struct.calcsize("Q") # 데이터   는 unsigned Long Long

# Function to receive video frames from the server
def receive_video():
    try:
        while True:
            while len(data) < payload_size:  # 수신 프레임은 데이터의 길이를 알려주는 헤더보다 커야함
                packet = client_socket.recv(1024 * 4)
                if not packet: # 없다면 연결종료
                    break
                else:
                    data += packet
            msg_size = struct.unpack("I", packet)[0]
            data = b""
            while len(data) < msg_size:
                packet = client_socket  .recv(4 * 1024)
                if not packet:
                    break
                data += packet
            frame_data = data
            frame = pickle.loads(frame_data)

            # Display the video frame from the server
            cv2.imshow("Video Stream", frame)

            frame = pickle.loads(frame_data)  # 바이트 스트림을 프레임으로 변환
            cv2.imshow("", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    except Exception as e:
        print(f"Error receiving video: {str(e)}")

# Function to display chat messages
def display_chat_message(message):
    chat_box.configure(state="normal")
    chat_box.insert(tk.END, message + '\n')
    chat_box.configure(state="disabled")
    chat_box.see(tk.END)
    message = chat_input.get()
    if message:
        chat_input.delete(0, tk.END)
        chat_message = f"CHAT:{message}"
        client_socket.send(chat_message.encode())
# Function to send chat messages to the server

# Function to prompt the user for a username
def get_username():
    while True:
        try:
            username = simpledialog.askstring("Username", "Enter your username:")
            if username:
                return username
        except Exception as e:
            print(f"Error getting username: {str(e)}")

def receive_chat():
    while True:
        try:
            message = client_socket.recv(1024)
            try:
                message = message.decode('utf-8')
            except UnicodeDecodeError:
                # Handle decoding error
                print("Error decoding chat message:", message)
                continue

            if message.startswith('CHAT:'):
                message = message[5:]
                display_chat_message(message)
        except Exception as e:
            print(f"Error receiving chat message: {str(e)}")

if __name__ == "__main__":
    # Connect to the video server
    client_socket.connect((host_ip, video_port))

    # Prompt the user f
    #
    # or a username
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

    # Start receiving video frames from the server
    video_thread = threading.Thread(target=receive_video)
    video_thread.start()

    # Start receiving chat messages from the server in a separate thread
    chat_thread = threading.Thread(target=receive_chat)
    chat_thread.start()

    # Start the Tkinter main loop
    client_window.mainloop()

