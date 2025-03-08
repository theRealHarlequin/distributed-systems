# python 3.11
# sample mqtt client code from https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# see also https://github.com/eclipse-paho/paho.mqtt.python/blob/master/docs/migrations.rst#versioned-the-user-callbacks

import random

from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883
topic = "spezialmessung/status"
# username = 'user'
# password = 'secure'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
