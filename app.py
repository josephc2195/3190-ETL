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
big_data = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/nba_2016_2017_100.csv")
attendance = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/attendance.csv")
player_stats = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/stats_and_salary.csv")
player_wikis = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/player_wikis.csv")
team_values = pd.read_csv("https://raw.githubusercontent.com/josephc2195/3190-ETL/master/Datasets/team_values.csv")

attendance.sort_values(by=["TEAM"], ascending=[True], inplace=True)
team_values.sort_values(by=["TEAM"], ascending=[True], inplace=True)

teams = attendance["TEAM"]
att_percent = attendance["PCT"]
val = team_values["VALUE_MILLIONS"]
player_stats["TWITTER_FOLLOWERS"] = big_data["TWITTER_FOLLOWER_COUNT_MILLIONS"]

total = 0
for num in att_percent:
        total += num
avg_attendance = total/30

selected = player_wikis[["names", "pageviews"]]
player_pageviews = selected.copy()
new_df = player_pageviews.groupby(["names"]).sum()
new_df.sort_values(by=["pageviews"], ascending=[False], inplace=True)
top_50 = new_df.head(50)
players_50 = top_50["names"]
pageviews_50 = top_50["pageviews"]

scatter_rpm_salary = px.scatter(player_stats, x="RPM", y="SALARY_MILLIONS", hover_name="PLAYER", hover_data=["SALARY_MILLIONS","RPM","POINTS","TRB","AST"])
scatter_rpm_salary.update_layout(
        xaxis_title="Real-Plus-Minus",
        yaxis_title="2016-2017 Salary"
)

scatter_followers_salary = px.scatter(player_stats, x="TWITTER_FOLLOWERS", y="SALARY_MILLIONS", hover_name="PLAYER", hover_data=["SALARY_MILLIONS", "TWITTER_FOLLOWERS"])
scatter_followers_salary.update_layout(
        xaxis_title="Twitter followers",
        yaxis_title="2016-2017 Salary"
)


app = dash.Dash(__name__)
server = app.server
app.title = "NBA Stats Dashboard"
topMenu = html.Header(role='banner', children=[
        html.Div([
                html.A("Tean stats", href="/", style={"padding":10}),
                html.A("Player stats", href="/players_breakdown")
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

players_page = html.Div(children=[
        html.H1("Top players"),
        html.H3("This graph shows the production of a player vs their salary"),
        dcc.Graph(figure=scatter_rpm_salary),
        html.H3("As we can see Lebron James was the most paid for the year, but also was by far the best player (according to Real Plus-Minus)"),
        html.Br(),

        html.H3("There are other factors that go into account when deciding a players salary."),
        html.H3("Does social media presense effect their compensation?"),
        dcc.Graph(figure=scatter_followers_salary),
        html.Br(),
        html.H3("Which players are the most popular in terms of pageviews?"),
        dcc.Graph(figure={
                'data': [
                        {'x': players_50, 'y': pageviews_50, 'type': 'bar', 'name': 'name'}
                ],
                'layout': {
                        'title': 'Top 50 popular players'
                }
        }),


])
@app.callback(Output(component_id="content", component_property="children"),
[Input(component_id='url', component_property="pathname")])
def display_page(pathname):
        if pathname =="/players_breakdown":
                return players_page
        else:
                return index_page


if __name__ == '__main__':
        app.run_server()