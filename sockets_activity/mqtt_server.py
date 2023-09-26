import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("cpu/temperature")

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic} Message: {str(msg.payload.decode('utf-8'))}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()