import paho.mqtt.client as mqtt
MQTT_BROKER = "0.tcp.in.ngrok.io"
MQTT_PORT = 17998
MQTT_TOPIC = "test_sensor_data"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def ring_buzzer():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    client.publish(MQTT_TOPIC, "RING_BUZZER")
    print("Publishing message...")
    client.loop_stop()
    client.disconnect()    