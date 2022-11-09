import time
import board
import busio
import adafruit_sgp40

# Set up IO
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Set up devices
# sgp
sgp = adafruit_sgp40.SGP40(i2c)

while True:
    print("Measurement: ", sgp.raw)
    print("")
    time.sleep(5)