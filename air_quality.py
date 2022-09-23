# This script captures data from the sensors and logs it.
# Todo: 
# 1. Capture data from all sensors
#   a. Deconflict I2C libraries (PM2.5 uses BUSIO but other use BOARD)
# 2. Log data to prevent memory filling
# 3. Create web dashboard for tracking

import time
import board
import busio
import serial
import adafruit_sgp40
import adafruit_scd4x
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C

# Set up IO
# i2c = board.I2C()  # uses board.SCL and board.SDA # From scp and sgp, I think same as following cmd
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Set up devices
# sgp
sgp = adafruit_sgp40(i2c)

# scd
scd4x = adafruit_scd4x.SCD4X(i2c)
scd4x.start_periodic_measurement()

#pm25
reset_pin = DigitalInOut(board.G0)
reset_pin.direction = Direction.OUTPUT
reset_pin.value = False
pm25 = PM25_I2C(i2c, reset_pin)

# Set up object to save data
class airQuality:
  pm10 = 0
  pm25 = 0
  co2 = 0
  temp = 0
  humid = 0
  voc = 0

# Stabilize readings
print("Waiting for readings to stabilize")
time.sleep(180) #pm25 requires 30 sec. SGP40 recommends several minutes before reading

# Read and log sensors
while True:
  # Read sensors
  # log sensors
  time.sleep(1)
