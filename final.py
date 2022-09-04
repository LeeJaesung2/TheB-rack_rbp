#! /usr/bin/python2
import time
import sys
import json
import RPi.GPIO as GPIO
import requests

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

input_prev = 0

#No.1 rack
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #IR

GPIO.setup(27,GPIO.OUT) #13_Green
GPIO.setup(22,GPIO.OUT) #15_Red

hx = HX711(20, 16)
#DT 20, SCK 16
hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(98)
#hx.set_reference_unit(referenceUnit)

GPIO.output(27,True)
GPIO.output(22,False)

#No.2 rack
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #IR_pinNum19

GPIO.setup(9,GPIO.OUT) #pinNum21_Green
GPIO.setup(11,GPIO.OUT) #pinNum23_Red

hx2 = HX711(5, 6)
#DT 5_pinNum29, SCK 6_pinNum31
hx2.set_reading_format("MSB", "MSB")

hx2.set_reference_unit(98)
#hx2.set_reference_unit(referenceUnit)

GPIO.output(9,True)
GPIO.output(11,False)

#No.3 rack
GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #IR_pinNum22

GPIO.setup(8,GPIO.OUT) #pinNum24_Green
GPIO.setup(7,GPIO.OUT) #pinNum26_Red

hx3 = HX711(23, 24)
#DT 23_pinNum16, SCK 24_pinNum18
hx3.set_reading_format("MSB", "MSB")

hx3.set_reference_unit(98)
#hx3.set_reference_unit(referenceUnit)

GPIO.output(8,True)
GPIO.output(7,False)

hx.reset()
hx.tare()
hx2.reset()
hx2.tare()
hx3.reset()
hx3.tare()

while 1:
    
    print("Tare done! Add weight now...")

    while True:
        try:          
            val = hx.get_weight(5)
            val2 = hx2.get_weight(5)
            val3 = hx3.get_weight(5)
            print('val1:', val)
            print('val2:', val2)
            print('val3:', val3)
            
            #Num1 rack
            if(val < 5):
                GPIO.output(27,True)
                GPIO.output(22,False)
                
                data = {
                        "position": 1,
                        "status": 0, # 0: empty / 1: full
                }
                url = "http://ec2-15-164-210-172.ap-northeast-2.compute.amazonaws.com:8000/status/"+str(data['position'])
                    
                #print(url)
                # Making a PATCH request
                r = requests.patch(url, data)
                    
                # check status code for response received
                # success code - 200
                #print(r)
                     
                # print content of request
                #print(r.content)
                #break
            
            elif(val > 500):
                input = GPIO.input(17)
                if input_prev != input:
                    print("detected", input)
                    input_prev = input
                    
                    GPIO.output(27,False)
                    GPIO.output(22,True)

                    data = {
                        "position": 1,
                        "status": 1, # 0: empty / 1: full
                    }
                    url = "http://ec2-15-164-210-172.ap-northeast-2.compute.amazonaws.com:8000/status/"+str(data['position'])
                    
                    #print(url)
                    # Making a PATCH request
                    r = requests.patch(url, data)
                     
                    # check status code for response received
                    # success code - 200
                    #print(r)
                     
                    # print content of request
                    #print(r.content)
                
                    hx.power_down()
                    hx.power_up()
                    time.sleep(1)
                else:
                    print("No.1 not detected", input)
                    time.sleep(1)
                    
            #num2 rack
            if(val2 < 5):
                GPIO.output(9,True)
                GPIO.output(11,False)
                
                data = {
                        "position": 2,
                        "status": 0, # 0: empty / 1: full
                }
                url = "http://ec2-15-164-210-172.ap-northeast-2.compute.amazonaws.com:8000/status/"+str(data['position'])
                    
                #print(url)
                # Making a PATCH request
                r = requests.patch(url, data)
                    
                # check status code for response received
                # success code - 200
                #print(r)
                     
                # print content of request
                #print(r.content)
                #break
            
            elif(val2 > 500):
                input2 = GPIO.input(10)
                if input_prev != input2:
                    print("detected", input2)
                    input_prev = input2
                    
                    GPIO.output(9,False)
                    GPIO.output(11,True)

                    data = {
                        "position": 2,
                        "status": 1, # 0: empty / 1: full
                    }
                    url = "http://ec2-15-164-210-172.ap-northeast-2.compute.amazonaws.com:8000/status/"+str(data['position'])
                    
                    #print(url)
                    # Making a PATCH request
                    r = requests.patch(url, data)
                     
                    # check status code for response received
                    # success code - 200
                    #print(r)
                     
                    # print content of request
                    #print(r.content)
                
                    hx2.power_down()
                    hx2.power_up()
                    time.sleep(1)
                else:
                    print("No2. not detected", input2)
                    time.sleep(1)
                    
            #num3 rack
            if(val3 < 5):
                GPIO.output(8,True)
                GPIO.output(7,False)
                
                data = {
                        "position": 3,
                        "status": 0, # 0: empty / 1: full
                }
                url = "http://ec2-15-164-210-172.ap-northeast-2.compute.amazonaws.com:8000/status/"+str(data['position'])
                    
                #print(url)
                # Making a PATCH request
                r = requests.patch(url, data)
                    
                # check status code for response received
                # success code - 200
                #print(r)
                     
                # print content of request
                #print(r.content)
                #break
            
            elif(val3 > 500):
                input3 = GPIO.input(25)
                if input_prev != input3:
                    print("detected", input3)
                    input_prev = input3
                    
                    GPIO.output(8,False)
                    GPIO.output(7,True)

                    data = {
                        "position": 3,
                        "status": 1, # 0: empty / 1: full
                    }
                    url = "http://ec2-15-164-210-172.ap-northeast-2.compute.amazonaws.com:8000/status/"+str(data['position'])
                    
                    #print(url)
                    # Making a PATCH request
                    r = requests.patch(url, data)
                     
                    # check status code for response received
                    # success code - 200
                    #print(r)
                     
                    # print content of request
                    #print(r.content)
                
                    hx3.power_down()
                    hx3.power_up()
                    time.sleep(1)
                else:
                    print("No3. not detected", input3)
                    time.sleep(1)
                
            time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
        
    