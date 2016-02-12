import spidev
import time

spi = spidev.SpiDev()

spi.open(0,1)

try:
    while True:
        resp = spi.xfer2([0xAA])
        time.sleep(0.5)
except KeyboardInterrupt:
    spi.close()
   
