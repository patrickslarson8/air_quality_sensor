from flask import Flask, render_template
import altair as alt
import sqlite3 as lite
import pandas as pd

# Create connection to database
conn = lite.connect('sensorsData.db', check_same_thread=False)

def get_top_data_as_df():
     cur = conn.cursor()
     cur.execute("SELECT * FROM SENSORS_data ORDER BY timestamp DESC LIMIT 10;")
     rows = cur.fetchall()
     rows = pd.read_sql("SELECT * FROM SENSORS_data ORDER BY timestamp DESC LIMIT 1000;",conn)
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
def index():
     rows = get_top_data()
     formatted_information = f" Date and time {rows[0][0]}\n Temperature: {rows[0][1]}\n Humidity {rows[0][2]}\n CO2: {rows[0][3]}\n VOC: {rows[0][4]}\n PM10: {rows[0][5]}\n PM25: {rows[0][6]}\n"
     return formatted_information

@app.route('/current')
def index2():
     rows = get_top_data()
     return rows

@app.route('/template')
def template():
     rows = get_top_data()
     #context = altair_temperature(rows)
     context = build_context(rows)
     return render_template('index.html', context = context)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
