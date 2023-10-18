import socket
import cv2
import pickle
import struct
import imutils
import threading

from network_programming_test.TCPsocket.video.video_server import server_socket

# Create a socket for the video server
video_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_host_ip = 'localhost'
video_port = 9000
video_server_socket.bind((video_host_ip, video_port))
video_server_socket.listen(5)

# Create a socket for the chat server
chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_host_ip = 'localhost'
chat_port = 9001
chat_server_socket.bind((chat_host_ip, chat_port))
chat_server_socket.listen(5)

# List to keep track of connected video clients
connected_video_clients = []

# List to keep track of connected chat clients
connected_chat_clients = []
# Function to handle video streaming for a single client
def handle_video(client_socket):
    vid = cv2.VideoCapture(0)
    if vid.isOpened():
        print("Camera is ready.")
    else:
        print("Error: Camera not found.")
        return

    while True:
        try:
            img, frame = vid.read()
            frame = imutils.resize(frame, width=640)
            frame_bytes = pickle.dumps(frame)
            msg = struct.pack("Q", len(frame_bytes)) + frame_bytes
            client_socket.sendall(msg)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        except Exception as e:
            print(f"Error handling video for {client_socket}: {str(e)}")
            break

    vid.release()
    client_socket.close()

# List to keep track of connected client sockets
connected_clients = []

# Function to distribute chat messages to all clients
def distribute_chat_message(message, sender_socket):
    for client_socket in connected_clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print(f"Error distributing chat message: {str(e)}")

# Function to handle chat messages for a single client
def handle_chat(client_socket):
    while True:
        try:
            chat_message = client_socket.recv(1024).decode()
            if not chat_message:
                break
            distribute_chat_message(chat_message, client_socket)
        except Exception as e:
            print(f"Error handling chat for {client_socket}: {str(e)}")
            break

# Accept and handle new client connections
def accept_clients():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"{client_address} connected")
        connected_clients.append(client_socket)

        # Create separate threads for video streaming and chat handling
        video_thread = threading.Thread(target=handle_video, args=(client_socket,))
        chat_thread = threading.Thread(target=handle_chat, args=(client_socket,))

        video_thread.start()
        chat_thread.start()

if __name__ == "__main__":
    # Start accepting clients in a separate thread
    accept_thread = threading.Thread(target=accept_clients)
    accept_thread.start()
    cv2.destroyAllWindows()  # Release OpenCV resources when done

    # Your server will continue to run and handle multiple clients concurrently.
