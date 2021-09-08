'''import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('clincian_data.csv')

fig = go.Figure()
fig.show()'''
import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv(
    'clinician_data.csv')
df.head()

scale = 500

fig = go.Figure()
fig.add_trace(go.Scattergeo(
    locationmode='USA-states',
    lon=df['longitude'],
    lat=df['latitude'],
    text=df['country'],
    marker=dict(
        size=df['availability'] * scale,
        cmax=1,
        cmin=0,
        color=df['availability'],
        line_width=0.5,
        sizemode='area',
        colorbar=dict(
            title="Availability"
        ),
        colorscale="Viridis"
    )))
fig.show()
