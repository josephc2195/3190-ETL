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

#player_stats = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/playerStats.csv")
#advanced_stats = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/AdvancedStats.csv")
attendance = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/attendance.csv")
sorted_by_points = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/stats_and_salary.csv")
#player_wikis = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/player_wikis.csv")
team_values = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/team_values.csv")

attendance.sort_values(by=["TEAM"], ascending=[True], inplace=True)
team_values.sort_values(by=["TEAM"], ascending=[True], inplace=True)
sorted_by_salary = sorted_by_points.sort_values(by=["SALARY_MILLIONS"], ascending=[False])

teams = attendance["TEAM"]
att_percent = attendance["PCT"]
val = team_values["VALUE_MILLIONS"]

total = 0
for num in att_percent:
        total += num
avg_attendance = total/30

scatter_rpm_salary = px.scatter(sorted_by_salary, x="RPM", y="SALARY_MILLIONS", hover_name="PLAYER", hover_data=["SALARY_MILLIONS","RPM","POINTS","TRB","AST"])

app = dash.Dash(__name__)
server = app.server
app.title = "NBA Stats Dashboard"
topMenu = html.Header(role='banner', children=[
        html.Div([
                html.A("Home", href="/", style={"padding":10}),
                html.A("Breakdown", href="/breakdown")
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
                        {'x': teams, 'y': att_percent, 'type': 'bar', 'name': 'name'}
                ],
                'layout': {
                        'title': 'Percentage of Attendance per team'
                }
        }),
        html.Br(),
        html.H2("Which team is the most valuable?"),
        dcc.Graph(figure={
                'data': [
                        {'x': teams, 'y': val, 'type':'bar', 'name': 'Team Value'}
                ],
                'layout': {
                        'title': 'Value of Team (In Millions)'
                }
        }),
])

breakdown = html.Div(children=[
        html.H1("Top players"),
        html.H3("This graph shows the production of a player vs their salary"),
        dcc.Graph(figure=scatter_rpm_salary),
        html.H3("As we can see Lebron James was the most paid for the year, but also was by far the best player (according to Real Plus-Minus)"),
        html.Br(),

        html.H3("Production on the court isn't the only measure of someones value to an NBA team. Lets see if popular players on social media have an affect on attendance which would be added revenue for a team.")

])
@app.callback(Output(component_id="content", component_property="children"),
[Input(component_id='url', component_property="pathname")])
def display_page(pathname):
        if pathname =="/breakdown":
                return breakdown
        else:
                return index_page


if __name__ == '__main__':
        app.run_server()