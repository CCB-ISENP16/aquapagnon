import json
import time
from datetime import datetime
import pigpio
# from influxdb import InfluxDBClient
from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector

# https://fr.pinout.xyz/pinout/wiringpi

# pin 4 data DS18B

class Sensor:
    def __init__(self, topic, name):
        super().__init__()
        self.__state = False
        self.__name = name
        self.__topic = topic
        self.__pi = pigpio.pi()

        self.__mqtt = MqttClient(
            self, "127.0.0.1", ["cmd/"+self.__topic/"POWER"], self.__name-"Sensor-")

    def Receive(self, server, topic: str, payload: bytes):
        print("")

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def Stop(self):
        print("[{}] closed".format("Sensor-"+self.__topic))

    def toggle(self):

