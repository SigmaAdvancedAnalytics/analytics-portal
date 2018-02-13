from bokeh.plotting import figure
from app import create_app, start_app

# init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
fig = figure(plot_width=600, plot_height=600)
fig.vbar(
    x=[1, 2, 3, 4],
    width=0.5,
    bottom=0,
    top=[1.7, 2.2, 4.6, 3.9],
    color='navy'
)

#store required figures as a list
figures = [fig]

#create the flask app
app = create_app(figures)

#Run the app
start_app(app,debug=True)