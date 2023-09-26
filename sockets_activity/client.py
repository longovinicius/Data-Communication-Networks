import socket
import time
import threading
import paho.mqtt.client as mqtt
import requests
import argparse


class MultiProtocol_Client:
    def __init__(self, protocol="UDP") -> None:
        self.data = []
        self.ip = None
        self.port = None
        self.x = None
        self.y = None
        self.protocol = protocol
        if self.protocol == "MQTT":
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.connect(self.ip, self.port, 60)
            self.mqtt_client.loop_start()

    def SETUP(self, IP, PORTA):
        self.ip = IP
        self.port = PORTA
    
    def RESET(self):
        self.data = []

    def SET_X(self, X):
        self.x = X

    def SET_Y(self, Y):
        self.y = Y

    def read_cpu_temperature(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = f.read().strip()
            return float(temp) / 1000.0
        except FileNotFoundError:
            return 0.0  
 
    def save_temperature(self):
        while True:
            start = time.perf_counter()
            self.data.append(self.read_cpu_temperature())
            elapsed = time.perf_counter() - start
            time.sleep(max(self.y - elapsed, 0))

    def send_average_temperature(self):
        if self.protocol == "UDP":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while True:
                start = time.perf_counter()
                if self.data:
                    average = sum(self.data) / len(self.data)
                    s.sendto(str(average).encode('utf-8'), (self.ip, self.port))
                elapsed = time.perf_counter() - start
                time.sleep(max(self.x - elapsed, 0))
        elif self.protocol == "MQTT":
            while True:
                start = time.perf_counter()
                if self.data:
                    average = sum(self.data) / len(self.data)
                    self.mqtt_client.publish("temperature", str(average))
                elapsed = time.perf_counter() - start
                time.sleep(max(self.x - elapsed, 0))
        elif self.protocol == "HTTP":
            while True:
                start = time.perf_counter()
                if self.data:
                    average = sum(self.data) / len(self.data)
                    requests.post(f"http://{self.ip}:{self.port}/temperature", data={"value": average})
                elapsed = time.perf_counter() - start
                time.sleep(max(self.x - elapsed, 0))

    def start(self):
        t1 = threading.Thread(target=self.save_temperature)
        t2 = threading.Thread(target=self.send_average_temperature)
        t1.start()
        t2.start()

# Example usage
parser = argparse.ArgumentParser(description="MultiProtocol Client")
parser.add_argument("--protocol", choices=["UDP", "MQTT", "HTTP"], default="UDP", help="Communication protocol")
parser.add_argument("--ip", type=str, default="127.0.0.1", help="Server IP address")
parser.add_argument("--port", type=int, default=12345, help="Server port number")
parser.add_argument("--x", type=int, default=5, help="Server X number")
parser.add_argument("--y", type=int, default=2, help="Server y number")

args = parser.parse_args()

client = MultiProtocol_Client(protocol=args.protocol)
client.SETUP(args.ip, args.port)
client.SET_X(args.x)
client.SET_Y(args.y)
client.start()