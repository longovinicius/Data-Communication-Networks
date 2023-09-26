import socket

def start_udp_server():
    host = 'localhost'
    port = 54321
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print(f"UDP Server listening on {host}:{port}")
    while True:
        data, addr = s.recvfrom(1024)
        print(f"Received data: {data.decode('utf-8'):.2f} from {addr}")

start_udp_server()