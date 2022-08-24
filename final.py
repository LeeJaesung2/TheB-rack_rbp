#! /usr/bin/python2
import time
import sys
import json
import datetime
import RPi.GPIO as GPIO

EMULATE_HX711=False
referenceUnit = 1

if not EMULATE_HX711:
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.setup(27,GPIO.OUT) #13_Green
GPIO.setup(22,GPIO.OUT) #15_Red

input_prev = 0


hx = HX711(20, 16)
#DT 20, SCK 16
hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(98)
#hx.set_reference_unit(referenceUnit)

GPIO.output(27,True)
GPIO.output(22,False)

while 1:

    hx.reset()
    hx.tare()
    print("Tare done! Add weight now...")

    while True:
        try:          
            val = hx.get_weight(5)
            print(val)
                
            if(val < -1):
                GPIO.output(27,True)
                GPIO.output(22,False)
                
                with open('bike.json', 'w') as outfile:
                    json.dump({
                    "position":1,
                    "holdingTime":None,
                    "holdingStatus":False
                    }, outfile)
                print("Make Json File!") 
                break
            elif(val > 300):
                input = GPIO.input(17)
                if input_prev != input:
                    print("detected", input)
                    
                    GPIO.output(27,False)
                    GPIO.output(22,True)
                    
                    now = datetime.datetime.now()
                    nowDatetime = now.strftime('%Y-%m-%d-%H-%M')
                        
                    with open('bike.json', 'w') as outfile:
                        json.dump({
                        "position":1,
                        "holdingTime":nowDatetime,
                        "holdingStatus":True
                        }, outfile)
                    print("Make Json File!")
                    time.sleep(5)
                
                    hx.power_down()
                    hx.power_up()
                    time.sleep(1)
                else:
                    print("not detected", input)
                    time.sleep(1)
            time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
        
    