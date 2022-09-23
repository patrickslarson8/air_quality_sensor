# This script captures data from the sensors and logs it.
# Todo: 
# 1. Capture data from all sensors
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
import sqlite3 as lite
import sys

# Connect to local database
con = lite.connect('sensorsData.db')

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
 
myAir = airQuality()

# Stabilize readings
print("Waiting for readings to stabilize")
time.sleep(180) #pm25 requires 30 sec. SGP40 recommends several minutes before reading

# Read and log sensors
with con:
  cur = con.cursor()
while True:
  # Read sensors
  # Get temp and humid readings first to be used in VOC
  myAir.temp = scd4x.temperature
  myAir.humid = scd4x.relative_humidity
  myAir.co2 = scd4x.CO2
  myAir.voc = sgp.measure_index(temperature=myAir.temp, relative_humidity=myAir.humid)
  aqdata = pm25.read()
  myAir.pm10 = aqdata["pm10 env"]
  myAir.pm25 = aqdata["pm25 env"]
  
  # log sensors
  # Table format is:
  # time, temp, humid, carbon, voc, pm10, pm25
  cur.execute("INSERT INTO SENSORS_data VALUES(datetime('now'), myAir.temp, myAir.humid,
              myAir.co2, myAir.voc, myAir.pm10, myAir.pm25)")
  
  # Sleep for timing interval
  time.sleep(1)
