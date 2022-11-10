# This script captures data from the sensors and logs it.
# Todo:
# 2. Log data to prevent memory filling
# 3. Create web dashboard for tracking

import time
import board
import busio
import serial
import adafruit_sgp40
import adafruit_scd4x
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.uart import PM25_UART
import sqlite3 as lite
import sys

# Connect to local database
con = lite.connect('database.db')

# Set up IO
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

reset_pin = None


# Set up devices
# sgp
sgp = adafruit_sgp40.SGP40(i2c)

# scd
scd4x = adafruit_scd4x.SCD4X(i2c)
scd4x.start_periodic_measurement()

#pm25
pm25 = PM25_UART(uart, reset_pin)

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
time.sleep(180)  # pm25 requires 30 sec. SGP40 recommends several minutes before reading

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
  newEntry = "INSERT INTO sensor_table (timestamp, temp, humid, carbon, voc, pm10, pm25) VALUES (datetime('now'), {}, {}, {}, {}, {}, {});".format(myAir.temp, myAir.humid, myAir.co2, myAir.voc, myAir.pm10, myAir.pm25)
  #print(newEntry) 
  cur.execute(newEntry)
  con.commit()
  
  # Sleep for timing interval
  time.sleep(60)
