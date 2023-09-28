import time
import psutil
import socket
import threading
from functools import reduce


class GenericClient:
    def __init__(self):
        self.tempList = []
        self.X = None
        self.Y = None
        self.ip = None
        self.port = None
        self.running = False
        # self.send_thread = None

    def SET_X(self, X):
        self.X = X

    def SET_Y(self, Y):
        self.Y = Y

    def RESET(self):
        self.tempList.clear()

    def GET_TEMPERATURE(self):
        try:
            sensors_temperatures = psutil.sensors_temperatures()
            if 'coretemp' in sensors_temperatures:
                core_temps = sensors_temperatures['coretemp']
                if core_temps:
                    temperature = core_temps[0].current
                else:
                    temperature = None
        except Exception as e:
            print("Erro ao obter temperatura da CPU:", e)
            temperature = None
        
        self.tempList.append(temperature)

        return temperature

    def GET_AVG_TEMPERATURE(self):
        len_ = float(len(self.tempList))
        if len_:
            return reduce(lambda t_a, t_b: t_a + t_b, self.tempList) / len_
        else:
            return None
    
    def SEND_AVG_TEMPERATURE(self):
        raise NotImplementedError(
            "Subclasses must implement the send_avg_temperature method")

    def SEND_TEMPERATURE(self):
        raise NotImplementedError(
            "Subclasses must implement the send_temperature method")

    def SETUP(self, IP, PORTA):
        raise NotImplementedError(
            "Subclasses must implement the setup method")

    def CONNECT(self):
        raise NotImplementedError(
            "Subclasses must implement the connect method")

    def DISCONNECT(self):
        raise NotImplementedError(
            "Subclasses must implement the disconnect method")


class SocketClient(GenericClient):
    def __init__(self):
        super().__init__()
        self.ip = None
        self.port = None
        self.running = False

    def SEND_AVG_TEMPERATURE(self):
        while self.running:
            start_time = time.time()
            avg_ = self.GET_AVG_TEMPERATURE()
            
            if avg_:
                data = "avgT = " + "{:.2f}".format(self.GET_AVG_TEMPERATURE()) + "°C"
            else:
                data = "avgT = None"
                
            self.socket.sendto(data.encode('utf-8'), (self.ip, self.port))            
            print("[Socket Client] Sent:\t", data, "\tat t = {:.2f}s".format(time.time() - self.initTime))

            time.sleep(self.X - (time.time() - start_time))

    def SEND_TEMPERATURE(self):
        while self.running:
            start_time = time.time()
            data = "T = " + "{:.2f}".format(float(self.GET_TEMPERATURE())) + "°C"
            
            self.socket.sendto(data.encode('utf-8'), (self.ip, self.port)) 
            print("[Socket Client] Sent:\t", data, "\t\tat t = {:.2f}s".format(time.time() - self.initTime))

            time.sleep(self.Y - (time.time() - start_time))

    def SETUP(self, IP, PORTA):
        self.ip = IP
        self.port = PORTA

    def CONNECT(self):
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.initTime = time.time()

        self.thread_temp = threading.Thread(target=self.SEND_TEMPERATURE)
        self.thread_temp.start()

        self.thread_avg_temp = threading.Thread(target=self.SEND_AVG_TEMPERATURE)
        self.thread_avg_temp.start()

        print(f"[Socket Client] Connected to {self.ip}: {self.port}")

    def DISCONNECT(self):
        self.running = False

        self.thread_avg_temp.join()
        self.thread_temp.join()
        self.socket.close()

        print(f"[Socket Client] Disconnected from {self.ip}: {self.port}")


class MQTTClient(GenericClient):
    def __init__(self, host, port, topic):
        super().__init__(host, port)
        self.topic = topic
        # Add MQTT-specific initialization here

    def connect(self):
        # Implement MQTT-specific logic to establish a connection
        print(f"Connected to MQTT broker at {self.ip}:{self.port}")

    def send_data(self, data):
        # Implement MQTT-specific logic to send data
        print(f"Sent data '{data}' to topic {self.topic}")

    def receive_data(self):
        # Implement MQTT-specific logic to receive data
        print("Received data from MQTT broker")

    def disconnect(self):
        # Implement MQTT-specific logic to disconnect
        print("Disconnected from MQTT broker")


class HTTPClient(GenericClient):
    def __init__(self, host, port, route):
        super().__init__(host, port)
        self.route = route
        # Add HTTP-specific initialization here

    def connect(self):
        # Implement HTTP-specific logic to establish a connection
        print(f"Connected to HTTP server at {self.ip}:{self.port}")

    def send_data(self, data):
        # Implement HTTP-specific logic to send data
        print(f"Sent data '{data}' to route {self.route}")

    def receive_data(self):
        # Implement HTTP-specific logic to receive data
        print("Received data from HTTP server")

    def disconnect(self):
        # Implement HTTP-specific logic to disconnect
        print("Disconnected from HTTP server")
