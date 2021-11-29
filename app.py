import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import os
import pandas as pd

cwd = os.getcwd()

playerStats = pd.read_csv(cwd + "/Datasets/playerStats.csv")
adStats = pd.read_csv(cwd + "/Datasets/advancedStats.csv")
