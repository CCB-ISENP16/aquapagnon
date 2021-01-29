import json
import time
import glob
from datetime import datetime
from threading import Thread


# from influxdb import InfluxDBClient
from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector

# https://fr.pinout.xyz/pinout/wiringpi

# pin 4 data DS18B


class DS18B20(Thread):
    def __init__(self, topic, name):
        super().__init__()
        self.__state = False
        self.__name = name
        self.__topic = topic
        self.__temperature = 0.0
        self.__base_dir = '/sys/bus/w1/devices/'
        self.__device_folder = glob.glob(self.__base_dir + '28*')[0]
        self.__device_file = self.__device_folder + '/w1_slave'

        self.__mqtt = MqttClient(
            self, "127.0.0.1", ["cmd/"+self.__topic+"/TEMP"], self.__name+"-DS18B20")

        self.__running = True
        self.start()

    def Receive(self, server, topic: str, payload: bytes):
        msg = payload.decode("utf-8")
        if msg == "":
            print("[MQTT] {} received at {} from {}".format(
                msg, topic, self.__name+"-WaterFlowSensor"))

            self.Send("stat/"+self.__topic+"/RESULT",
                      str(round(self.__temperature, 1)) + " °C")

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def read_temp_raw(self):
        f = open(self.__device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def run(self):
        while self.__running:
            time.sleep(5)
            self.__temperature = self.read_temp()
            self.Send("stat/"+self.__topic+"/RESULT",
                      str(round(self.__temperature, 1)) + " °C")

    def Stop(self):
        self.__running = False
        self.join()
        self.__mqtt.Halt()
        print("[{}] closed".format("Sensor-"+self.__topic))
        print("Stop DS18B20")
