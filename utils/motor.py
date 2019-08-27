import RPi.GPIO as GPIO
import time

# set up GPIO output channel, we set GPIO4 (Pin 7) to OUTPUT
channels = 4

class Motor():
    def __init__(self):
        # to use Raspberry Pi board pin numbers
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(channels, GPIO.OUT)

    def __del__(self):
        GPIO.cleanup(channels)

    # time : vibration time 
    def active(self, duration):
        GPIO.output(channels, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(channels, GPIO.LOW)

if __name__ == "__main__":
    start_motor = Motor()
    start_motor.active(3)
