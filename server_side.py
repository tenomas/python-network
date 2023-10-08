import socket
import cv2
import pickle
import struct
import imutils
import threading

from network_programming_test.TCPsocket.video.video_server import vid

# Define global variables for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = 'localhost'  # Server IP address
port = 9000
server_socket.bind((host_ip, port))
server_socket.listen(5)
print("Waiting for clients...")

# List to keep track of connected client sockets
connected_clients = []

# Function to handle video streaming for a single client
def handle_video(client_socket):
    vid = cv2.VideoCapture(0)
    if not vid.isOpened():
        print("Error: Camera not found.")
        return

    print("Camera is ready.")
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

# Function to accept and handle new client connections
def accept_clients():
    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr} connected")
        connected_clients.append(client_socket)
        video_thread = threading.Thread(target=handle_video, args=(client_socket,))
        video_thread.start()

if __name__ == "__main__":
    # Start accepting clients in a separate thread
    accept_thread = threading.Thread(target=accept_clients)
    accept_thread.start()

    # Display the camera feed on the server's screen
    while True:
        img, frame = vid.read()
        frame = imutils.resize(frame, width=640)
        cv2.imshow("Server Camera Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
