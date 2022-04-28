import paho.mqtt.client as mqtt
from config import MQTT_HOST, MQTT_PORT, SECTION
from logger import logger

class MQTT():
    def __init__(self) -> None:
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.connect(MQTT_HOST, MQTT_PORT, keepalive=36000)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT connected")
        else:
            logger.error("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        logger.info("MQTT Disconnected")

    def on_publish(self, client, userdata, mid):
        pass
    
    def make_machine_topic(self, machine):
        return f"{SECTION}/switch/{machine}"

