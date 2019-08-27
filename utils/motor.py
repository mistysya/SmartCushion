import RPi.GPIO as GPIO
import time

# set up GPIO output channel, we set GPIO4 (Pin 7) to OUTPUT
channels = [7]

class motor():
    def __init__(self):
        # to use Raspberry Pi board pin numbers
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(channels, GPIO.OUT)

    def __del__(self):
        GPIO.cleanup(channels)

    # time : vibration time 
    def active(self, time):
        GPIO.output(channels[0], GPIO.HIGH)
        time.sleep(time)
        GPIO.output(channels[0], GPIO.LOW)

if __name__ == "__main__":
    start_motor = motor()
    start_moter.active(3)
