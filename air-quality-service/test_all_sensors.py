import time
import board
import busio
import serial
import adafruit_sgp40
import adafruit_scd4x
from adafruit_pm25.uart import PM25_UART



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

# pm25
pm25 = PM25_UART(uart, reset_pin)

time.sleep(33)

while True:
    # Read sensors
    # Get temp and humid readings first to be used in VOC
    temp = scd4x.temperature
    print("Temp: {}".format(temp))
    humid = scd4x.relative_humidity
    print("humid: {}".format(humid))
    print("CO2: {}".format(scd4x.CO2))
    print("VOC: {}".format(sgp.measure_index(temperature=temp, relative_humidity=humid)))
    aqdata = pm25.read()
    print("pm10: {}".format(aqdata["pm10 env"]))
    print("pm2.5: {}".format(aqdata["pm25 env"]))

    # Sleep for timing interval
    time.sleep(5)