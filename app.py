from flask import Flask
# from datetime import datetime
# app = Flask(__name__)

# @app.route('/')
# def homepage():
#     the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

#     return """
#     <h1>Hello heroku</h1>
#     <p>It is currently {time}.</p>

#     <img src="http://loremflickr.com/600/400" />
#     """.format(time=the_time)

# if __name__ == '__main__':
#     app.run(debug=True, use_reloader=True)


import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc 
import dash_html_components as html 
import random
import plotly
import plotly.graph_objs as go 
from collections import deque


X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)

server = Flask(__name__)
app = dash.Dash(__name__, server = server)
app.layout = html.Div(children = [
	html.H1("Live graph example"),
	dcc.Graph(id = "live-graph", animate=True),
	dcc.Interval(id = "graph-update", interval=1000)

	])

@app.callback(Output("live-graph", "figure"),
				events = [Event("graph-update", "interval")])
def update_graph():
	global X
	global Y
	X.append(X[-1]+1)
	Y.append(Y[-1]+(Y[-1]*random.uniform(-0.1,0.1)))
	data = go.Scatter(x = list(X), 
						y = list(Y),
						name = "Scatter plot",
						mode = "lines+markers")   # this mode is for making scatter plot a line graph
	return {"data": [data], "layout": go.Layout(xaxis = dict(range=[min(X), max(X)]),
												yaxis = dict(range=[min(Y), max(Y)]))}


if __name__ == "__main__":
	app.run_server(debug=True, threaded=True)

