import socket
import time
from utils import read_cpu_temperature


def send_udp_data():
    host = '200.135.75.49'
    port = 54321
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        temperature = read_cpu_temperature()  # Função fictícia para ler a temperatura da CPU
        s.sendto(temperature.encode('utf-8'), (host, port))
        time.sleep(1)

send_udp_data()