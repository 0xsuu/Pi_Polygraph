
import smbus
import time
import RPi.GPIO as GPIO

#ADC Manual:
#  init with I2C Address, port name(JP*)
#  read data using readData()
class ADC():
    def __init__(self, i2cAddress, portName):
        self._bus = smbus.SMBus(1)
        self._i2cAddress = i2cAddress
        if portName == "JP4":
            self._port = 0x10
        elif portName == "JP5":
            self._port = 0x20
        elif portName == "JP6":
            self._port = 0x40
        elif portName == "JP7":
            self._port = 0x80

    def _convert(self, tmp):
        return ((tmp&0xff)<<8 |(tmp>>8))&0x0FFF #reversed and zeroed out first 4 bits

    def readData(self):
        self._bus.write_byte(self._i2cAddress, self._port)
        tmp = self._bus.read_word_data(self._i2cAddress, 0x00)
        return self._convert(tmp)

