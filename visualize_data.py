import plotly.graph_objects as go
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from pseudo_data import *

# read CSVs into dataframes
caregiver_df = pd.read_csv('clinician_data.csv')
caregiver_distances_df = pd.read_csv('caregiver_distances.csv')

# define scale for marker sizes
scale = 500
caregiver_df['text'] = caregiver_df['country'] + '<br>User Type: Caregiver'

fig = go.Figure()

# add caregiver user data
fig.add_trace(go.Scattergeo(
    locationmode='USA-states',
    lon=caregiver_df['longitude'],
    lat=caregiver_df['latitude'],
    text=caregiver_df['text'],
    marker=dict(
        size=caregiver_df['availability'] * scale,
        cmax=1,
        cmin=0,
        color=caregiver_df['availability'],
        line_width=0,
        sizemode='area',
        colorbar=dict(
            title="Caregiver Availability"
        ),
        colorscale="mint"
    )))

# add caregiver distances data
for i in range(len(caregiver_distances_df)):
    if float(caregiver_distances_df['distance'].min()) / float(caregiver_distances_df['distance'][i]) > 0.25:
        fig.add_trace(
            go.Scattergeo(
                locationmode='USA-states',
                lon=[caregiver_distances_df['patient_lon'][i],
                     caregiver_distances_df['caregiver_lon'][i]],
                lat=[caregiver_distances_df['patient_lat'][i],
                     caregiver_distances_df['caregiver_lat'][i]],
                mode='lines',
                line=dict(width=2, color='red'),
                opacity=float(caregiver_distances_df['distance'].min(
                )) / float(caregiver_distances_df['distance'][i]),
            )
        )

fig.update_layout(
    title_text='MedECC Caregiver Matchmaking Visualization<br>(Hover for Caregiver Country and Location)',
    showlegend=False,
    geo=dict(
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
    ),
)
fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig),
    html.Button('Generate New Patient', id='gen-patient', n_clicks=0),
    html.Div(id='num-patients-added',
             children='')
])

@app.callback(Output('num-patients-added', 'children'),
              Input('gen-patient', 'n_clicks'))
def add_patient(n_clicks):
    user_data = generate_user()
    return '{} new patients have been added'.format(
        n_clicks
    )


app.run_server(debug=True, use_reloader=False)
