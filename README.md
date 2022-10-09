# Air Quality Sensor

A small air quality sensor that measures various 
aspects and logs them for later analysis.
Measures: VOC, C02, temperature, PM2.5, and humidity

## Hardware

Raspberry Pi
Adafruit SGP40 (https://learn.adafruit.com/adafruit-sgp40/python-circuitpython)  
Adafruit SCD-40 (https://learn.adafruit.com/adafruit-scd-40-and-scd-41/python-circuitpython)  
Adafruit PM 2.5 Sensor (https://learn.adafruit.com/pm25-air-quality-sensor)  

## How to use

1. Download repo
2. Install requirements

~~~bash
sudo apt-get install sqlite3 python3-pip
~~~

3. Install requirements.txt

~~~bash
pip3 install -r requirements.txt
~~~

4. Create SQLite database

~~~bash
sqlite3 sensorsData.db
sqlite> BEGIN;
sqlite> CREATE TABLE SENSORS_data (timestamp DATETIME, temp NUMERIC, humid NUMERIC, carbon NUMERIC, voc NUMERIC, pm10 NUMERIC, pm25 NUMERIC, note TEXT);
sqlite> COMMIT;
~~~

5. Configure air_quality.py and webserver.py to autostart

- Open air_quality.service in a text editor and ensure the two locations for ExecStart point to your python interpretor and air_quality.py locations
- Copy air_quality.service to /lib/systemd/system/
- Add the correct permissions to the service file

~~~bash
sudo chmod 644 /lib/systemd/system/air_quality.service
~~~

- Configure service to start

~~~bash
sudo systemctl daemon-reload
sudo systemctl enable air_quality.service
sudo reboot
~~~

## Todo list

### Set up database

### Set up webserver

(https://medium.com/@rovai/from-data-to-graph-a-web-jorney-with-flask-and-sqlite-6c2ec9c0ad0)  
1. Create webpage
2. Create webserver
3. Update page with data from DB
