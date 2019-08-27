import RPi.GPIO as GPIO
import time

# set up GPIO output channel, we set GPIO4 (Pin 7) to OUTPUT
channels = 7

class motor():
    def __init__(self):
        # to use Raspberry Pi board pin numbers
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(channels, GPIO.OUT)

    def __del__(self):
        GPIO.cleanup(7)

    # time : vibration time 
    def active(self, duration):
        GPIO.output(channels, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(channels, GPIO.LOW)

if __name__ == "__main__":
    start_motor = motor()
    start_motor.active(3)
