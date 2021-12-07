import plotly.graph_objects as go
import numpy as np
from colors import hues, cold_grays, neutral_grays, warm_grays, colors

fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>Hues</b>', '<b>Cold</b>', '<b>Neutral</b>', '<b>Warm</b>'],
    line_color='white', fill_color='white',
    align='center', font=dict(color='black', size=22)
  ),
  cells=dict(
    values=[list(hues), list(cold_grays), list(neutral_grays), list(warm_grays)],
    line_color=[list(hues.values()), list(cold_grays.values()), list(neutral_grays.values()), list(warm_grays.values())],
    fill_color=[list(hues.values()), list(cold_grays.values()), list(neutral_grays.values()), list(warm_grays.values())],
    align='center',
    font=dict(color=[[colors['warm_black']]*10, [colors['warm_white']]*5 + [colors['warm_black']]*5], size=22),
    height=60
    ))
])

fig.show()