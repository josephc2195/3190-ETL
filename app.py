from pandas.io.parquet import to_parquet
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import os
import pandas as pd

cwd = os.getcwd()

player_stats = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/playerStats.csv")
advanced_stats = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/AdvancedStats.csv")
attendance = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/attendance.csv")
stats_and_salaries = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/stats_and_salary.csv")


teams = attendance.loc["0":, "TEAM"].values.tolist()
att_percent = attendance.loc["0":, "PCT"].values.tolist()

app = dash.Dash(__name__)
server = app.server
app.title = "Dashboard"
topMenu = html.Header(role='banner', children=[
        html.Div([
                html.A("Home", href="/")
        ])
])

app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        topMenu,
        html.Div(id="content")
])
index_page = html.Div(children=[
        html.H1("Which are the most popular teams?"),
        html.Br(),
        dcc.Graph(figure={
                'data': [
                        {'x': teams, 'y': att_percent, 'type': 'bar', 'name': 'name'},
                ],
                'layout': {
                        'title': 'Percentage of Attendance per team'
                }
        }),

        html.H2("Second Graph"),

        

])

@app.callback(Output(component_id="content", component_property="children"),
[Input(component_id='url', component_property="pathname")])
def display_page(pathname):
        if pathname =="/page-1":
                return page_1_layout
        else:
                return index_page


if __name__ == '__main__':
        app.run_server()