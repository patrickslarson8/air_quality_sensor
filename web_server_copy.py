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
    chart = alt.Chart(data).transform_fold(
    ['daily new cases', 'daily new recovered', 'daily new deaths']
    )
    line = chart.mark_line().encode(
    x='date:T',
    y=alt.Y('value:Q', axis=alt.Axis(title='# of cases')),
    color='key:N',
    tooltip=['yearmonthdate(date)','daily new cases',
      'daily new recovered', 'daily new deaths']
    ).properties(width=700)
    chart_json = line.to_json()
    return chart_json

def altair_temperature(df):
     chart = alt.Chart(df)
     line = chart.mark_line().encode(x = 'timestamp:T', y='temp:Q')
     chart_json = line.to_json()
     return chart_json


if __name__ == '__main__':
    print(altair_temperature(get_top_data()))
