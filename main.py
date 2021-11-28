import os
import pandas as pd

cwd = os.getcwd()

playerStats = pd.read_csv(cwd + "/Datasets/playerStats.csv")
