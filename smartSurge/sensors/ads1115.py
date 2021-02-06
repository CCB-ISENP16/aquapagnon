import json
import time
import glob

# from influxdb import InfluxDBClient
from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector

# https://fr.pinout.xyz/pinout/wiringpi

# pin 4 data DS18B


class ADS1115():
    def __init__(self, topic, name):
        super().__init__()
        self.__state = False
        self.__name = name
        self.__topic = topic
        self.__temperature = 0.0
        self.__voltage0 = 0.0
        self.__voltage1 = 0.0
        self.__base_dir = '/sys/bus/iio/devices/'
        self.__device_folder = glob.glob(self.__base_dir + 'iio*')[0]

        self.__in_voltage0_raw = self.__device_folder + '/in_voltage0_raw'
        self.__in_voltage1_raw = self.__device_folder + '/in_voltage1_raw'

        self.__voltage0_scale = self.__device_folder + '/in_voltage0_scale'
        self.__voltage1_scale = self.__device_folder + '/in_voltage1_scale'

        self.__mqtt = MqttClient(
            self, "127.0.0.1", ["cmnd/"+self.__topic+"/VOLT0", "cmnd/"+self.__topic+"/VOLT1"], "Sensor-"+self.__name+"-ADS1115")

    def Receive(self, server, topic: str, payload: bytes):
        msg = payload.decode("utf-8")
        print("[MQTT] {} received at {} from {}".format(
            msg, topic, "Sensor-"+self.__name+"-ADS1115"))

        if topic == "cmnd/"+self.__topic+"/VOLT0":
            self.__voltage0 = self.read_volatage0()
            self.Send("stat/"+self.__topic+"/RESULT0",
                      str(round(self.__voltage0, 2)))

        if topic == "cmnd/"+self.__topic+"/VOLT1":
            self.__voltage1 = self.read_volatage1()
            self.Send("stat/"+self.__topic+"/RESULT1",
                      str(round(self.__voltage1, 2)))

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def read_voltage0_scale(self):
        f = open(self.__voltage0_scale, 'r')
        lines = f.readlines()
        f.close()
        return float(lines[0].rstrip("\n"))

    def read_volatge0_raw(self):
        f = open(self.__in_voltage0_raw, 'r')
        lines = f.readlines()
        f.close()
        return float(lines[0].rstrip("\n"))

    def read_volatage0(self):
        rawVolatage = self.read_volatge0_raw()
        scale = self.read_voltage0_scale()
        voltage = rawVolatage * scale / 1000
        return voltage

    def read_voltage1_scale(self):
        f = open(self.__voltage1_scale, 'r')
        lines = f.readlines()
        f.close()
        return float(lines[0].rstrip("\n"))

    def read_volatge1_raw(self):
        f = open(self.__in_voltage1_raw, 'r')
        lines = f.readlines()
        f.close()
        return float(lines[0].rstrip("\n"))

    def read_volatage1(self):
        rawVolatage = self.read_volatge1_raw()
        scale = self.read_voltage1_scale()
        voltage = rawVolatage * scale / 1000
        return voltage

    def Stop(self):
        print("[Thread] {} Stopped".format(self.__name))
        self.__mqtt.Halt()
