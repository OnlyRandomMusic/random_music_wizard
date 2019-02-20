import RPi.GPIO as GPIO
# import time

pin_number = 0

GPIO.setup(pin_number, GPIO.OUT)


pwm = GPIO.PWM(pin_number, 100)  # 100 is the frequency of the PWM signal
pwm.start(50)  # value in percent

# pwm.ChangeDutyCycle(duty_cycle)
