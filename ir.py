import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.OUT)

GPIO.output(27,False)
input_prev = 0

while 1:
    input = GPIO.input(17)
    print(input)
    if input_prev != input:
        print("input : ", input)
        input_prev = input

    if input == 1:
        GPIO.output(27,True)
    else:
        GPIO.output(27,False)
