import socket
import cv2
import pickle
import struct

#소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = 'localhost' #서버 IP 주소
port = 9000
client_socket.connect((host_ip,port)) # 서버와 연결
data = b""
payload_size = struct.calcsize("Q") # 데이터는 unsigned Long Long

while True:
    while len(data) < payload_size: # 수신 프레임은 데이터의 길이를 알려주는 헤더보다 커야함
        packet = client_socket.recv(1024*4)
        if not packet: #없다면 연결종료
            break
        else:
            data += packet
        packed_msg_size = data[:payload_size] #프레임 길이 추출
        data = data[payload_size:] # 프레임 추출
        msg_size = struct.unpack("Q",packed_msg_size)[0] # 프레임 길이를 파이썬 형태로 변환

        while len(data) < msg_size: # 길이 만큼 프레임 수신
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size] # 한 프레임 만큼 얻음
        data = data[msg_size:] # 다음

        frame  = pickle.loads(frame_data) # 바이트 스트림을 프레임으로 변환
        cv2.imshow("",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
client_socket.close()