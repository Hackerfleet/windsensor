import network
from mqtt import MQTTClient 
import machine 
import time 
 
def sub_cb(topic, msg): 
   print(msg) 
 
wlan = network.WLAN(network.STA_IF) 
wlan.active(True)

#wlan.connect("c-base-botnet", auth=(WLAN.WPA2, "wifipassword"), timeout=5000) 
 
while not wlan.isconnected():  
    machine.idle() 
print("Connected to Wifi\n") 
 
client = MQTTClient("windsensor_0", "192.168.178.98",user="", password="", port=1883) 
#client = MQTTClient("windsensor_0", "mqtt.cbrp3.c-base.org",user="", password="", port=1883) 
client.set_callback(sub_cb) 
client.connect()
client.subscribe(topic="/hackerfleet/sensors/windsensor/control") 

print("Connected to MQTT")

speedInterrupts = 0
directionInterrupts = 0

speedTicks = 0
directionTicks = 0

def callbackSpeed(pin):
    global speedInterrupts
    speedInterrupts += 1

def callbackDirection(pin):
    global directionInterrupts
    directionInterrupts += 1

speedPin = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)
directionPin = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)

speedPin.irq(trigger=machine.Pin.IRQ_FALLING, handler=callbackSpeed)
directionPin.irq(trigger=machine.Pin.IRQ_FALLING, handler=callbackSpeed)

print("Pin setup done")

while True:

    if speedInterrupts > 0 or directionInterrupts > 0:
        state = machine.disable_irq()
        if speedInterrupts > 0:
            speedTicks += 1
            speedInterrupts -= 1
        if directionInterrupts > 0:
            directionTicks += 1
            directionInterrupts -= 1

        machine.enable_irq(state)

        print("Direction: ", str(directionTicks), " Speed: ", str(speedTicks))

