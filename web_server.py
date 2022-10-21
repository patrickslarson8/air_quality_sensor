from flask import Flask, render_template
import altair as alt
import sqlite3 as lite
import pandas as pd

# Create connection to database
conn = lite.connect('sensorsData.db', check_same_thread=False)

# Get information from database into a dataframe
selectStatement = "SELECT * FROM SENSORS_data;"
data = pd.read_sql_query(selectStatement, conn)

def get_top_data():
     cur = conn.cursor()
     cur.execute("SELECT * FROM SENSORS_data ORDER BY timestamp DESC LIMIT 10;")
     rows = cur.fetchall()
     rows = pd.read_sql("SELECT * FROM SENSORS_data ORDER BY timestamp DESC LIMIT 10;",
     conn)
     return rows

## For reference
def altair_global_timeseries(data):
    base = alt.Chart(data).transform_fold(
    ['daily new cases', 'daily new recovered', 'daily new deaths']
    )
    line = base.mark_line().encode(
    x='date:T',
    y=alt.Y('value:Q', axis=alt.Axis(title='# of cases')),
    color='key:N',
    tooltip=['yearmonthdate(date)','daily new cases',
      'daily new recovered', 'daily new deaths']
    ).properties(width=700)
    chart_json = line.to_json()
    return chart_json

def altair_temperature(df):
     base = alt.Chart(df)
     line = base.mark_line().encode(x = 'timestamp', y='temp')
     chart_json = line.to_json()
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
     context = altair_temperature(rows)
     return render_template('index.html', context = context)



if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
