from flask import Flask
import altair as alt

#todo
#data = read from database


# base = alt.Chart(data).transform_fold(
#     ['temperature', 'humidity', 'carbon dioxide, VOCs, particulate 1.0, particulate 2.5']
# )
# line = base.mark_line().encode(
#     x='date:T',
#     y=alt.Y('value:Q', axis=alt.Axis(title='air quality')),
#     color='key:N',
#     tooltip=['yearmonthdate(date)']
# ).properties(width=700)
#
# line

app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')