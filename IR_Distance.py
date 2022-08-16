import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)

sensor = 17

#GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)
GPIO.setwarnings(False)

PIN_TRIGGER = 7
PIN_ECHO = 11

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.output(PIN_TRIGGER, GPIO.LOW)

print ("Waiting for sensor to settle")
time.sleep(2)

try:
    while(1):
        #print(GPIO.input(sensor))
        if(GPIO.input(sensor)==GPIO.LOW):
            print("Motion detected!")
            time.sleep(0.5)
            
            #print ("Calculating distance")
        
            GPIO.output(PIN_TRIGGER, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(PIN_TRIGGER, GPIO.LOW)
              
            while GPIO.input(PIN_ECHO)==0:
                pulse_start_time = time.time()
            while GPIO.input(PIN_ECHO)==1:
                pulse_end_time = time.time()

            pulse_duration = pulse_end_time - pulse_start_time
            distance = round(pulse_duration * 17150, 2)
            print ("Distance:",distance,"cm")

            
        else:
            print("motion not detected")
            time.sleep(0.5)
        
finally:
      GPIO.cleanup()