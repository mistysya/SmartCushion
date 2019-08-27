import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class SensorDataCollector():

    def __init__(self):
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D5)

        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)

        # create an analog input channel on pin 0
        self.chan0 = AnalogIn(mcp, MCP.P0)
        self.chan1 = AnalogIn(mcp, MCP.P1)
        self.chan2 = AnalogIn(mcp, MCP.P2)
        self.chan3 = AnalogIn(mcp, MCP.P3)
        self.chan4 = AnalogIn(mcp, MCP.P4)
        self.chan5 = AnalogIn(mcp, MCP.P5)
        self.chan6 = AnalogIn(mcp, MCP.P6)

    def get_sensor_data(self):
        try:
#        print('Raw-channel0: ', chan0.value)
#        print('Raw-channel1: ', chan1.value)
#        print('Raw-channel2: ', chan2.value)
#        print('Raw-channel3: ', chan3.value)
#        print('Raw-channel4: ', chan4.value)
#        print('Raw-channel5: ', chan5.value)
#        print('Raw-channel6: ', chan6.value)
#        print('----------------------------')
            data = [self.chan0.value, self.chan1.value, self.chan2.value, self.chan3.value,
                    self.chan4.value, self.chan5.value, self.chan6.value]
            print(data)
            return data
        except Exception:
            print('[Exception]: ' + str(Exception))

if __name__ == '__main__':
    fsr = SensorDataCollector()
    while True:
        fsr.get_sensor_data()
        time.sleep(1)
