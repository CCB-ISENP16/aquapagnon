import json
import time
from datetime import datetime

import pigpio
# from influxdb import InfluxDBClient
from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector

# https://fr.pinout.xyz/pinout/wiringpi

# 23 / 24


class Feeder:
    def __init__(self, topic, name, powerPinNumber, manualPinNumber):
        super().__init__()

        self.__state = "OFF"
        self.__name = name
        self.__topic = topic
        self.__powerPinNumber = powerPinNumber
        self.__manualPinNumber = manualPinNumber
        self.__pi = pigpio.pi()

        try:
            if self.__pi.connected:
                self.__pi.set_mode(self.__manualPinNumber, pigpio.OUTPUT)
                self.__pi.set_mode(self.__powerPinNumber, pigpio.OUTPUT)
                self.__pi.write(self.__manualPinNumber, pigpio.LOW)
                self.__pi.write(self.__powerPinNumber, pigpio.LOW)

        except Exception as ex:
            print("[GPIO] Failed initializing GPIO. Exception: {}".format(ex))

        self.__mqtt = MqttClient(
            self, "127.0.0.1", ["cmnd/"+self.__topic+"/POWER"], "Feeder-"+self.__name)
        self.powerUp_Down()

    def Receive(self, server, topic: str, payload: bytes):
        msg = payload.decode("utf-8")

        print("[MQTT] {} received at {} from {}".format(
            msg, topic, self.__name+"-Petacc"))

        if msg == "on":
            self.__state = "ON"
            self.__state = msg.upper()
            self.powerUp_Down()
            time.sleep(5)
            self.feeding()
            time.sleep(15)
            self.powerUp_Down()
            self.__state = "OFF"

        if msg == "off":
            self.__state = msg.upper()
            self.powerUp_Down()
            self.__state = "OFF"

        if msg == "":
            self.Send("stat/"+self.__topic+"/RESULT", self.__state)

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def Stop(self):
        self.__pi.stop()
        print("[pigpio] {} Stopped".format(self.__name))
        self.__mqtt.Halt()

    def powerUp_Down(self):
        self.__pi.write(self.__powerPinNumber, pigpio.HIGH)
        print("pin set to high level")
        time.sleep(3)
        self.__pi.write(self.__powerPinNumber, pigpio.LOW)
        print("pin set to low level")
        self.Send("stat/"+self.__topic+"/RESULT", self.__state)

    def feeding(self):
        self.__pi.write(self.__manualPinNumber, pigpio.HIGH)
        time.sleep(0.5)
        self.__pi.write(self.__manualPinNumber, pigpio.LOW)
