import socket
import cv2
import threading

# Create a socket for video streaming
video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the video socket to a specific IP address and port
video_host = 'localhost'
video_port = 9000
video_socket.bind((video_host, video_port))

# Listen for incoming video connections
video_socket.listen(5)
print(f"Video server is listening on {video_host}:{video_port}")

# Create a socket for chat
chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the chat socket to a specific IP address and port
chat_host = 'localhost'
chat_port = 9001
chat_socket.bind((chat_host, chat_port))

# Listen for incoming chat connections
chat_socket.listen(5)
print(f"Chat server is listening on {chat_host}:{chat_port}")

# List to keep track of connected client sockets for video and chat
connected_clients_video = []
connected_clients_chat = []

# Function to distribute chat messages to all clients
def distribute_chat_message(message, sender_socket):
    for client_socket in connected_clients_chat:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                # Handle any socket errors or disconnections here
                print(f"Error sending message to client: {e}")
                connected_clients_chat.remove(client_socket)

# Function to handle a client connection for video streaming
def handle_client_video(client_socket):
    print(f"Video Connected: {client_socket.getpeername()}")

    # Add the client socket to the list of connected clients for video
    connected_clients_video.append(client_socket)

    vid = cv2.VideoCapture(0)

    while True:
        try:
            ret, frame = vid.read()

            # Serialize the frame
            _, frame_data = cv2.imencode('.jpg', frame)
            frame_bytes = frame_data.tobytes()

            # Send the video frame to all clients for video streaming
            for client in connected_clients_video:
                try:
                    client.sendall(frame_bytes)
                except Exception as e:
                    # Handle any socket errors or disconnections here
                    print(f"Error sending video frame: {e}")
                    connected_clients_video.remove(client)

            # Receive and process chat messages
            chat_message = client_socket.recv(1024).decode()
            if chat_message.startswith("CHAT:"):
                chat_message = chat_message[5:]  # Remove "CHAT:" prefix
                distribute_chat_message(f"Client: {chat_message}", client_socket)

        except Exception as e:
            # Handle any socket errors or client disconnections here
            print(f"Video Client disconnected: {e}")
            connected_clients_video.remove(client_socket)
            client_socket.close()
            break

# Function to handle a client connection for chat
def handle_client_chat(client_socket):
    print(f"Chat Connected: {client_socket.getpeername()}")

    # Add the client socket to the list of connected clients for chat
    connected_clients_chat.append(client_socket)

    while True:
        try:
            chat_message = client_socket.recv(1024).decode()
            if chat_message.startswith("CHAT:"):
                chat_message = chat_message[5:]  # Remove "CHAT:" prefix
                distribute_chat_message(f"Client: {chat_message}", client_socket)
        except Exception as e:
            # Handle any socket errors or client disconnections here
            print(f"Chat Client disconnected: {e}")
            connected_clients_chat.remove(client_socket)
            client_socket.close()
            break

# Accept incoming video connections and create a new thread for each client
while True:
    client_socket_video, _ = video_socket.accept()
    video_thread = threading.Thread(target=handle_client_video, args=(client_socket_video,))
    video_thread.start()

# Accept incoming chat connections and create a new thread for each client
while True:
    client_socket_chat, _ = chat_socket.accept()
    chat_thread = threading.Thread(target=handle_client_chat, args=(client_socket_chat,))
    chat_thread.start()

