from outlets.outlet import Outlet
from sensors.ds18b20 import DS18B20
from sensors.fs300a import FS300A
import time

heater = Outlet(topic="heater", name="Heater", pinNumber=17)
light = Outlet(topic="light", name="Light", pinNumber=18)
ds18b20 = DS18B20(topic="thermometer", name="Thermometer")
fs300a = FS300A(pinNumber=20, topic="FS300A", name="WaterSensorFlow")
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        heater.Stop()
        light.Stop()
        ds18b20.Stop()
        fs300a.Stop()
        break
