import time
from threading import Thread


from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector

# https://fr.pinout.xyz/pinout/wiringpi


class SEN0161V2 (Thread):
    def __init__(self, topic, name):
        super().__init__()
        self.__topic = topic
        self.__name = name
        self.__pH = 0.0
        self.__acidVoltage = 2032.44
        self.__neutralVoltage = 1500.0
        self.__voltage = 0.0
        self.__mqtt = MqttClient(
            self, "127.0.0.1", ["stat/ADS1115/RESULT0", "cmnd/" + self.__topic + "/pH"], "Sensor-" + self.__name + "-SEN0161V2")
        self.readFile()
        self.__running = True
        self.start()

    def run(self):
        while self.__running == True:
            time.sleep(1)
            self.getpH()
            self.Send("stat/"+self.__topic+"/RESULT",
                      str(round(self.__pH, 1)) + " pH")

    def Receive(self, server, topic: str, payload: bytes):
        msg = payload.decode("utf-8")
        print("[MQTT] {} received at {} from {}".format(
            msg, topic, self.__name+"-SEN0161V2"))

        if topic == "stat/ADS1115/RESULT0":
            self.__voltage = float(msg)
            self.__voltage = self.__voltage * 1000

        if topic == "cmnd/" + self.__topic + "/pH":

            if msg == "":
                self.Send("stat/"+self.__topic+"/RESULT",
                          str(round(self.__pH, 1)) + " pH")
            else:
                self.Send("stat/"+self.__topic+"/RESULT",
                          str(round(self.__pH, 1)))

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def getpH(self):
        self.Send("cmnd/ADS1115/VOLT0", "getVoltage")
        time.sleep(0.5)
        slope = (7.0-4.0)/((self.__neutralVoltage-1500.0) /
                           3.0 - (self.__acidVoltage-1500.0)/3.0)
        intercept = 7.0 - slope*(self.__neutralVoltage-1500.0)/3.0
        phValue = slope*(self.__voltage-1500.0)/3.0+intercept
        round(phValue, 1)
        self.__pH = phValue

    def readFile(self):
        try:
            f = open("calibration/phdatas.txt", "r")
            self.__neutralVoltage = f.readline()
            self.__neutralVoltage = self.__neutralVoltage.rstrip(
                'neutralVoltage=')
            self.__neutralVoltage = float(self.__neutralVoltage)

            self.__acidVoltage = f.readline()
            self.__acidVoltage = self.__acidVoltage.rstrip("acidVoltage=")
            self.__acidVoltage = float(self.__acidVoltage)
        except:
            print("[sensor] Error while trying to open file phdata.txt")

    def Stop(self):
        self.__running = False
        self.join()
        print("[Thread] {} Stopped".format(self.__name))
        self.__mqtt.Halt()
