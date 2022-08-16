import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)

sensor = 17

GPIO.setup(sensor, GPIO.IN)
GPIO.setwarnings(False)
GPIO.setup(sensor,GPIO.IN)
print("wating for sensor")
time.sleep(1)

while(True):
    print(GPIO.input(sensor))
    if(GPIO.input(sensor)==GPIO.LOW):
        print("Motion detected!")
        time.sleep(0.5)
    else:
        print("motion not detected")
        time.sleep(0.5)
    time.sleep(0.1)