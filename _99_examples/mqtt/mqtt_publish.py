# python 3.11
# sample mqtt client code from https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# see also https://github.com/eclipse-paho/paho.mqtt.python/blob/master/docs/migrations.rst#versioned-the-user-callbacks

import time

from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883
topic = "spezialmessung/status"
# username = 'user'
# password = 'secure'

def connect_mqtt():
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


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Sent `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
