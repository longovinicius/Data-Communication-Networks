import time
import psutil
import socket
import threading
from functools import reduce
import paho.mqtt.client as mqtt


class GenericServer:
    def __init__(self):
        self.ip = None
        self.port = None
        self.running = False

    def SETUP(self, IP, PORTA):
        raise NotImplementedError("Subclasses must implement the setup method")

    def START(self):
        raise NotImplementedError("Subclasses must implement the start method")

    def STOP(self):
        raise NotImplementedError("Subclasses must implement the stop method")


class SocketServer(GenericServer):
    def __init__(self):
        super().__init__()
        self.socket = None
        
    def SETUP(self, IP, PORTA):
        self.ip = IP
        self.port = PORTA
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
        print(f"[Socket Server] Listening on IP {self.ip}, PORT {self.port}")

    def START(self):
        self.running = True
        print(f"[Socket Server] Running, press 'c' to stop")

        while (self.running):
            data, addr = self.socket.recvfrom(1024)
            print(f"[Socket Server] Received: {data.decode('utf-8')} from {addr}")

    def STOP(self):
        print("[Socket Server] Stopped.")
        self.socket.close()


class MQTTServer(GenericServer, mqtt.Client):
    def __init__(self):
        super().__init__()
        self.topic = None

    def SETUP(self, IP, PORTA, TOPIC):
        self.ip = IP
        self.port = PORTA
        self.topic = TOPIC
        
#     def START(self):
#         self.running = True
#         self.subscribe(self.topic)
#         self.connect(self.ip, self.port)
#         self.on_message(lambda client, userdata, message: )
        
#         print(f"MQTT Server started on {self.ip}:{self.port} with topic {self.topic}")

#         while (self.running):
#             temperature = message.payload.decode("utf-8")
#             data, addr = self.socket.recvfrom(1024)
#             print(f"[MQTT Server] Received: {data.decode('utf-8')} from {addr}")

#         self.loop_forever()
#         # Implement MQTT-specific logic to start the server

#     def STOP(self):
#         # Implement MQTT-specific logic to stop the server
#         print("MQTT Server stopped")



# def on_message(client, userdata, msg):
#     print(f"Topic: {msg.topic} Message: {str(msg.payload.decode('utf-8'))}")

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect("localip", 1883, 60)

# client.loop_forever()

class HTTPServer(GenericServer):
    def __init__(self, ip, port, route):
        super().__init__(ip, port)
        self.route = route
        # Add HTTP-specific initialization here

    def START(self):
        # Implement HTTP-specific logic to start the server
        print(
            f"HTTP Server started on {self.ip}:{self.port} with route {self.route}")

    def STOP(self):
        # Implement HTTP-specific logic to stop the server
        print("HTTP Server stopped")
