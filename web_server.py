from flask import Flask, render_template
import altair as alt
import sqlite3 as lite
import pandas as pd

# Create connection to database
conn = lite.connect('sensorsData.db', check_same_thread=False)

# Get information from database into a dataframe
selectStatement = "SELECT * FROM SENSORS_data;"
data = pd.read_sql_query(selectStatement, conn)

base = alt.Chart(data).transform_fold(
     ['temperature', 'humidity', 'carbon dioxide, VOCs, particulate 1.0, particulate 2.5'])
line = base.mark_line().encode(
    x='date:T',
    y=alt.Y('value:Q', axis=alt.Axis(title='air quality')),
    color='key:N',
    tooltip=['yearmonthdate(date)']
    ).properties(width=700)

line

app = Flask(__name__)
#@app.route('/')
#def index():
#    #ploting
#    plot_global_cases_per_country = altair_plot.altair_global_cases_per_country(final_df)
#    plot_global_time_series = altair_plot.altair_global_time_series(
#        timeseries_final)
#    plot_geo_analysis = altair_plot.altair_geo_analysis(final_df)
#    context = {'plot_global_cases_per_country': plot_global_cases_per_country,
#               'plot_global_time_series': plot_global_time_series, 'plot_geo_analysis': plot_geo_analysis}
#    return render_template('index.html', context=context)

@app.route('/')
def index():
     cur = conn.cursor()
     cur.execute("SELECT * FROM SENSORS_data ORDER BY timestamp DESC LIMIT 10;")
     rows = cur.fetchall()
     formatted_information = f" Date and time {rows[0][0]}\n Temperature: {rows[0][1]}\n Humidity {rows[0][2]}\n CO2: {rows[0][3]}\n VOC: {rows[0][4]}\n PM10: {rows[0][5]}\n PM25: {rows[0][6]}\n"
     return formatted_information

@app.route('/current')
def index2():
     cur = conn.cursor()
     cur.execute("SELECT * FROM SENSORS_data ORDER BY timestamp DESC LIMIT 1;")
     rows = cur.fetchall()
     return rows

@app.route('/template')
def template():
     cur = conn.cursor()
     cur.execute("SELECT * FROM SENSORS_data ORDER BY timestamp DESC LIMIT 10;")
     rows = cur.fetchall()
     context = f" Date and time {rows[0][0]}\n Temperature: {rows[0][1]}\n Humidity {rows[0][2]}\n CO2: {rows[0][3]}\n VOC: {rows[0][4]}\n PM10: {rows[0][5]}\n PM25: {rows[0][6]}\n"
     return render_template('index.html', context = context)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
