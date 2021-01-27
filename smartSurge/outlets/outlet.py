import json
import time
from datetime import datetime

import pigpio
# from influxdb import InfluxDBClient
from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector

# https://fr.pinout.xyz/pinout/wiringpi

# 18 / 17 / 27 / 22


class Outlet:
    def __init__(self, topic, name, pinNumber):
        super().__init__()

        self.__state = ""
        self.__name = name
        self.__topic = topic
        self.__pinNumber = pinNumber
        self.__pi = pigpio.pi()

        try:
            if self.__pi.connected:
                self.__pi.set_mode(self.__pinNumber, pigpio.OUTPUT)

        except Exception as ex:
            print("[GPIO] Failed initializing GPIO. Exception: {}".format(ex))

        self.__mqtt = MqttClient(
            self, "127.0.0.1", ["cmnd/"+self.__topic+"/POWER"], self.__name+"-Outlet")

    def Receive(self, server, topic: str, payload: bytes):
        msg = payload.decode("utf-8")

        print("[MQTT] {} received at {} from {}".format(
            msg, topic, self.__name+"-Outlet"))

        if msg == "on":
            self.__state = msg
            self.turnOn()

        if msg == "off":
            self.__state = msg
            self.turnOff()

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def Stop(self):
        print("[{}] closed".format("Outlet-"+self.__topic))

    def turnOff(self):
        self.__pi.write(self.__pinNumber, pigpio.LOW)
        print("pin set to low level")
        self.Send("stat/"+self.__topic+"RESULT", self.__state)

    def turnOn(self):
        self.__pi.write(self.__pinNumber, pigpio.HIGH)
        print("pin set to high level")
        self.Send("stat/"+self.__topic+"RESULT", self.__state)
