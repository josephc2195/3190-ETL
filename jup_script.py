import pandas as pd
from bokeh.io import show, output_notebook
from bokeh.models import CategoricalColorMapper, ColumnDataSource, FactorRange
from bokeh.plotting import figure, output_file
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

player_stats = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/playerStats.csv")
advanced_stats = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/AdvancedStats.csv")
attendance = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/attendance.csv")
stats_and_salaries = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/stats_and_salary.csv")

teams = attendance.loc["0":, "TEAM"].values.tolist()
att_percent = attendance.loc["0":, "PCT"].values.tolist()


fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]

p = figure(x_range=fruits, plot_height=250, toolbar_location=None, title="Fruit Counts")
p.vbar(x=fruits, top=counts, width=0.9)
p.xgrid.grid_line_color = None
p.y_range.start = 0
output_notebook()
show(p)