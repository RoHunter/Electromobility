import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)


GPIO.output(23, GPIO.HIGH)
GPIO.output(21, GPIO.HIGH)
GPIO.output(8, GPIO.HIGH)
GPIO.output(16, GPIO.HIGH)
GPIO.output(7, GPIO.HIGH)
GPIO.output(20, GPIO.HIGH)

GPIO.output(7, GPIO.HIGH)

GPIO.setup(26, GPIO.IN)