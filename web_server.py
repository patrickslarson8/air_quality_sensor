from flask import Flask
import altair as alt

#todo
#data = read from database
base = alt.Chart(data).transform_fold(
    ['temperature', 'humidity', 'carbon dioxide, VOCs, particulate 1.0, particulate 2.5']
)
line = base.mark_line().encode(
    x='date:T',
    y=alt.Y('value:Q', axis=alt.Axis(title='air quality')),
    color='key:N',
    tooltip=['yearmonthdate(date)']
).properties(width=700)

line
