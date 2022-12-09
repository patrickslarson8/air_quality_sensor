from flask import Flask, render_template
import altair as alt
import sqlite3 as lite
import pandas as pd
import os

# Create connection to database
# TODO: fix this path when going to back to deployment on RPi
conn = lite.connect('air-quality-service\\database.db', check_same_thread=False)

def get_top_data_as_df():
     rows = pd.read_sql("SELECT * FROM sensor_table ORDER BY timestamp DESC LIMIT 100;",conn)
     return rows

def get_all_as_df():
     rows = pd.read_sql("SELECT * FROM sensor_table ORDER BY timestamp DESC;",conn)
     return rows

#TODO: Develop sql statements
def get_daily_as_df():
     return pd.read_sql("SELECT * FROM sensor_table WHERE ROWID % 1440 = 0 ORDER BY timestamp DESC;",conn)

def get_weekly_as_df():
     return pd.read_sql("SELECT * FROM sensor_table WHERE ROWID % 10080 = 0 ORDER BY timestamp DESC;",conn)

def get_monthly_as_df():
     return pd.read_sql("SELECT * FROM sensor_table WHERE ROWID % 43800 = 0 ORDER BY timestamp DESC;",conn)

def get_every_nth_row_as_df(n):
     cur = conn.cursor()
     statement = 'SELECT *, ROWNUMBER() OVER (ORDER BY timestamp) as rownum FROM SENSORS_data WHERE rownum % {0} == 0 ORDER BY timestamp DESC;'.format(n)
     rows = pd.read_sql("statement",conn)
     return rows

def altair_temperature(df):
     base = alt.Chart(df)
     line = base.mark_line().encode(x = 'timestamp:T', y='temp:Q')
     chart_json = line.to_json()
     return chart_json

def altair_temp_and_humid(df):
     base = alt.Chart(df).encode(
          alt.X('timestamp:T')
     )

     line_A = base.mark_line(color='#5276A7').encode(
     alt.Y('temp:Q', axis=alt.Axis(titleColor='#5276A7'))
     )

     line_B = base.mark_line(color='#F18727').encode(
     alt.Y('humid:Q', axis=alt.Axis(titleColor='#F18727'))
     )

     base = alt.layer(line_A, line_B).resolve_scale(y='independent')
     return base

def altair_voc_co2(df):
     base = alt.Chart(df).encode(
     alt.X('timestamp:T')
     )

     line_A = base.mark_line(color='#5276A7').encode(
     alt.Y('voc:Q', axis=alt.Axis(titleColor='#5276A7'))
     )

     line_B = base.mark_line(color='#F18727').encode(
     alt.Y('carbon:Q', axis=alt.Axis(titleColor='#F18727'))
     )

     base = alt.layer(line_A, line_B).resolve_scale(y='independent')
     return base

def altair_particulate_25_10(df):
     base = alt.Chart(df).encode(
     alt.X('timestamp:T')
     )

     line_A = base.mark_line(color='#5276A7').encode(
     alt.Y('pm25:Q', axis=alt.Axis(titleColor='#5276A7'))
     )

     line_B = base.mark_line(color='#F18727').encode(
     alt.Y('pm10:Q', axis=alt.Axis(titleColor='#F18727'))
     )

     base = alt.layer(line_A, line_B).resolve_scale(y='shared')
     return base


app = Flask(__name__)

@app.route('/')
def home():
     rows = get_top_data_as_df()
     chart0 = altair_temp_and_humid(rows).to_json()
     chart1 = altair_voc_co2(rows).to_json()
     chart2 = altair_particulate_25_10(rows).to_json()
     return render_template('index.html', chart0 = chart0, chart1 = chart1, chart2 = chart2)

#TODO
@app.route('/daily')
def get_daily_template():
     rows = get_daily_as_df()
     chart0 = altair_temp_and_humid(rows).to_json()
     chart1 = altair_voc_co2(rows).to_json()
     chart2 = altair_particulate_25_10(rows).to_json()
     return render_template('index.html', chart0 = chart0, chart1 = chart1, chart2 = chart2)

#TODO
@app.route('/weekly')
def get_weekly_template():
     rows = get_weekly_as_df()
     chart0 = altair_temp_and_humid(rows).to_json()
     chart1 = altair_voc_co2(rows).to_json()
     chart2 = altair_particulate_25_10(rows).to_json()
     return render_template('index.html', chart0 = chart0, chart1 = chart1, chart2 = chart2)

#TODO
@app.route('/monthly')
def get_monthly_template():
     rows = get_monthly_as_df()
     chart0 = altair_temp_and_humid(rows).to_json()
     chart1 = altair_voc_co2(rows).to_json()
     chart2 = altair_particulate_25_10(rows).to_json()
     return render_template('index.html', chart0 = chart0, chart1 = chart1, chart2 = chart2)


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
