from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook"

key_path = './loppi-engineering-1be70e65caa0.json'

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

query_dp = """
SELECT
    *
FROM sandbox.teste2
WHERE timestamp >= '2022-01-23'
ORDER BY timestamp DESC
"""

results = client.query(query_dp).to_dataframe()

monitor = pd.DataFrame([{
    'cliente':row[1].client,
    'timestamp':row[1].timestamp,
    'cold_chamber_name':row[1].cold_chamber_name,
#     't_valve': row[1].temperature[0],
#     't_evap':row[1].temperature[1],
    'T_entrada_evaporador':row[1].temperature[2] if len(row[1].temperature)>2 else None,
    'T_ambiente':row[1].temperature[3] if len(row[1].temperature)>2 else None,
} for row in results.iterrows()]).sort_values('timestamp', ascending=False)


monitor_melted = pd.melt(monitor[monitor.timestamp > '2022-02-06', id_vars = ['cliente', 'timestamp', 'cold_chamber_name'])

fig = px.line(monitor_melted, x='timestamp', y='value', color='variable')
fig.update_xaxes(rangeslider_visible=True)


st.header('Doce Paladar - Camera Inferior')
st.plotly_chart(fig)
