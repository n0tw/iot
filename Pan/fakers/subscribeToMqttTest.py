import paho.mqtt.client as mqtt

def connect_mqtt():
    client = mqtt.Client()
    client.connect("150.140.186.118", 1883)
    return client

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("json/busstopmonitoring/urn:ngsi-ld:CrowdFlowObserved:Station:1")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

def run():
    client = connect_mqtt()
    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()

if __name__ == "__main__":
    run()

