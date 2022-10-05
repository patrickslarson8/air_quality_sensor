from flask import Flask
import altair as alt
import sqlite3 as lite
import pandas as pd

# Create connection to database
conn = lite.connect('sensorsData.db')

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
@app.route('/')
def index():
    # total confirmed cases globally
    total_all_confirmed = total_confirmed[total_confirmed.columns[-1]].sum()
    total_all_recovered = total_recovered[total_recovered.columns[-1]].sum()
    total_all_deaths = total_death[total_death.columns[-1]].sum()
    #ploting
    plot_global_cases_per_country = plotly_plot.plotly_global_cases_per_country(
        final_df)
    plot_global_time_series = plotly_plot.plotly_global_timeseries(
        timeseries_final)
    plot_geo_analysis = plotly_plot.plotly_geo_analysis(final_df)
    context = {"total_all_confirmed": total_all_confirmed,
               "total_all_recovered": total_all_recovered, "total_all_deaths": total_all_deaths,
            'plot_global_cases_per_country': plot_global_cases_per_country,
            'plot_global_time_series': plot_global_time_series,'plot_geo_analysis': plot_geo_analysis}
    return render_template('index.html', context=context)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
