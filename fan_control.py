import RPi.GPIO as GPIO
# import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin_number = 0

GPIO.setup(pin_number, GPIO.OUT)


pwm = GPIO.PWM(pin_number, 100)  # 100 is the frequency of the PWM signal
pwm.start(50)  # value in percent

duty_cycle = input()
pwm.ChangeDutyCycle(float(duty_cycle))

duty_cycle = input()

pwm.ChangeDutyCycle(float(duty_cycle))

input()

GPIO.cleanup()

