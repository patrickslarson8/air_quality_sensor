# Air Quality Sensor
A small air quality sensor that measures various 
aspects and logs them for later analysis.
Measures: VOC, C02, temperature, PM2.5, and humidity

## Hardware
Raspberry Pi
Adafruit SGP40 (https://learn.adafruit.com/adafruit-sgp40/python-circuitpython)  
Adafruit SCD-40 (https://learn.adafruit.com/adafruit-scd-40-and-scd-41/python-circuitpython)  
Adafruit PM 2.5 Sensor (https://learn.adafruit.com/pm25-air-quality-sensor)  

## todo
### Setting up SGP40 (I2C)
1. Install adafruit-blinka library
2. Install Circuit-python SGP40 library (https://github.com/adafruit/Adafruit_CircuitPython_SGP40)
3. Use sensor, see example code

### Setting up SCD-40 (I2C)
1. Install CircuitPyton SCD40 library (https://github.com/adafruit/Adafruit_CircuitPython_SCD4X)
2. Use sensor, see example code

### Setting up PM2.5 (UART)
1. Disable Pi serial console and enable serial port in Raspi-Config
2. install CircuitPyton PM2.5 library (https://github.com/adafruit/Adafruit_CircuitPython_PM25)
3. Use sensor

### Set up database
#### 1. Install SQLite
Install sudo apt-get install sqlite3
#### 2. Make local database
sqlite3 sensorsData.db  
sqlite> BEGIN;  
sqlite> CREATE TABLE SENSORS_data (timestamp DATETIME,  temp NUMERIC, humid NUMERIC, carbon NUMERIC, voc NUMERIC, pm10 NUMERIC, pm25 NUMERIC);  
sqlite> COMMIT;  

### Set up webserver
1. Create webpage
2. Create webserver
3. Update page with data from DB
