import time
import pigpio
from threading import Thread


from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector


class FS300A (Thread):
    def __init__(self, pinNumber, topic, name, fakeSensor=False):
        super().__init__()
        self.__pinNumber = pinNumber
        self.__topic = topic
        self.__name = name
        self.__counter = 0
        self.__PWMforFake = 21
        self.__flowRate = 0.0
        self.__pi = pigpio.pi()
        try:
            if self.__pi.connected:
                self.__pi.set_mode(self.__pinNumber, pigpio.INPUT)
                self.__CB = self.__pi.callback(
                    self.__pinNumber, pigpio.RISING_EDGE, self.updateCounter)

        except Exception as ex:
            print("[GPIO] Failed initializing GPIO. Exception: {}".format(ex))
        self.__mqtt = MqttClient(
            self, "127.0.0.1", ["cmd/"+self.__topic+"/FLOWRATE"], self.__name+"-FS300A")

        self.__running = True
        if fakeSensor == True:
            self.fakeFlowRate()
        self.start()

    def run(self):
        while self.__running == True:
            self.__counter = 0
            time.sleep(1)
            self.getFlowRate()
            self.Send("stat/"+self.__topic+"/RESULT",
                      str(int(self.__flowRate)) + " L/Min")

    def Receive(self, server, topic: str, payload: bytes):
        msg = payload.decode("utf-8")
        if msg == "":
            print("[MQTT] {} received at {} from {}".format(
                msg, topic, self.__name+"-WaterFlowSensor"))

            self.Send("stat/"+self.__topic+"/RESULT",
                      str(round(self.__flowRate, 1)) + " L/Min")

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def getFlowRate(self):
        self.__flowRate = (self.__counter * 60 / 5.5)

    def fakeFlowRate(self):
        print("[FS300A] Start PWM to Fake sensor")
        self.__pi.set_PWM_dutycycle(self.__PWMforFake, 128)
        self.__pi.set_PWM_frequency(self.__PWMforFake, 2)

    def updateCounter(self, gpio, level, _):
        self.__counter = self.__counter + 1

    def Stop(self):
        self.__running = False
        self.join()
        self.__CB.cancel()
        self.__mqtt.Halt()
        print("[{}] closed".format("FS300A-"+self.__topic))
        self.join()
        print("Stop FS300A")
