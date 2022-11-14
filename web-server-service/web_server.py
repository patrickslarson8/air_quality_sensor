from flask import Flask, render_template
import altair as alt
import sqlite3 as lite
import pandas as pd

# Create connection to database
conn = lite.connect('../air-quality-service/database.db', check_same_thread=False)

def get_top_data_as_df():
     rows = pd.read_sql("SELECT * FROM sensor_table ORDER BY timestamp DESC LIMIT 100;",conn)
     return rows

def get_all_as_df():
     rows = pd.read_sql("SELECT * FROM sensor_table ORDER BY timestamp DESC;",conn)
     return rows

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

## Create new context with several lines/charts
## TODO
def build_context(df):
     base = alt.Chart(df)
     temp_line = base.mark_line().encode(x = 'timestamp:T', y='temp:Q')
     hum_line = base.mark_ine().endcode(x = 'timestamp:T', y='humid:q')
     chart_json = temp_line.to_json()
     return chart_json

app = Flask(__name__)

@app.route('/')
def template():
     rows = get_top_data_as_df()
     chart = alt.vconcat(altair_temp_and_humid(rows), altair_voc_co2(rows))
     chart = alt.vconcat(chart, altair_particulate_25_10(rows))
     chart.properties(width='container',height='container')
     context = chart.to_json()
     return render_template('index.html', context = context)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
