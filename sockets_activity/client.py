import socket
import time
import threading

class UDP_Client:
    def __init__(self) -> None:
        self.data = []
        self.ip = None
        self.port = None
        self.x = None
        self.y = None

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
            return 0.0  # Return a default value
 
    def save_temperature(self):
        while True:
            start = time.perf_counter()
            self.data.append(self.read_cpu_temperature())
            elapsed = time.perf_counter() - start
            time.sleep(max(self.y - elapsed, 0))

    def send_average_temperature(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            start = time.perf_counter()
            if self.data:
                average = sum(self.data) / len(self.data)
                s.sendto(str(average).encode('utf-8'), (self.ip, self.port))
            elapsed = time.perf_counter() - start
            time.sleep(max(self.x - elapsed, 0))

    def start(self):
        t1 = threading.Thread(target=self.save_temperature)
        t2 = threading.Thread(target=self.send_average_temperature)
        t1.start()
        t2.start()

# Example usage
client = UDP_Client()
client.SETUP("127.0.0.1", 12345)
client.SET_X(5)
client.SET_Y(2)
client.start()
