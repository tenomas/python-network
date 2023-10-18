import socket
import cv2
import pickle
import struct
import imutils
import socket
import tkinter as tk
from threading import Thread

#소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9000
server_addr = ('',port)
#주소와 포트번호 바인드
server_socket.bind(server_addr)
#접속대기
server_socket.listen(5)
print("접속대기",server_addr)
#클라이언트 연결
while True:
    client_socket, addr = server_socket.accept()
    print(addr,'와 연결됨')
    if client_socket:
        vid = cv2.VideoCapture(0) # 웹캠 연결
        if vid.isOpened():
            print(vid.get(3),vid.get(4))
        while vid.isOpened():
            img, frame = vid.read() #프레임 획득
            frame = imutils.resize(frame,width=640) #프레임 크기 조절
            frame_bytes = pickle.dumps(frame) #프레임을 바이트 스트림으로 변환
            msg = struct.pack("Q",len(frame_bytes)) + frame_bytes
            # 메시지 Q unsigned long long d으로 보낼 데이터 크기 전송
            client_socket.sendall(msg)

            cv2.imshow('',frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
# List to keep track of connected client sockets
connected_clients = []

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
def send():
    message = message_entry.get()
    client_socket.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('server_ip', server_port)  # Replace with your server's IP and port
client_socket.connect(server_address)

# Create the chat GUI
root = tk.Tk()
root.title("Chat Client")

message_listbox = tk.Listbox(root)
message_listbox.pack()

message_entry = tk.Entry(root)
message_entry.pack()

send_button = tk.Button(root, text="Send", command=send)
send_button.pack()

# Start a thread to receive messages
receive_thread = Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

root.mainloop()