import time
import board
import busio
import adafruit_scd4x

# Set up IO
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# scd
scd4x = adafruit_scd4x.SCD4X(i2c)
scd4x.start_periodic_measurement()

while True:
  # Read sensors
  # Get temp and humid readings first to be used in VOC
  print(scd4x.temperature)
  print(scd4x.relative_humidity)
  print(scd4x.CO2)
  time.sleep(5)