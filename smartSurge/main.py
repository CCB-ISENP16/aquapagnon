from outlets.outlet import Outlet
import time

heater = Outlet(topic="heater", name="Heater", pinNumber=17)
light = Outlet(topic="light", name="Light", pinNumber=18)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        heater.Stop()
        light.Stop()
        break
