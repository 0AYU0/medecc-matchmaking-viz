import plotly.graph_objects as go

import pandas as pd

# read CSVs into dataframes
patient_df = pd.read_csv('patient_data.csv')
caregiver_df = pd.read_csv('clinician_data.csv')

# define scale for marker sizes
scale = 500
patient_df['text'] = patient_df['country'] + '<br>User Type: Patient'
caregiver_df['text'] = caregiver_df['country'] + '<br>User Type: Caregiver'

fig = go.Figure()

# add data from patient CSVs
fig.add_trace(go.Scattergeo(
  locationmode='USA-states',
  lon=patient_df['longitude'],
  lat=patient_df['latitude'],
  text=patient_df['text'],
  marker=dict(
      size=5,
      color='rgb(255,182,193)',
      line_width=0,
      sizemode='area',
  )))
# add data from caregiver CSVs
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
fig.show()
