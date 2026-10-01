"""Interactive dashboard for the IBM 56-row SpaceX sample."""
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
data = pd.read_csv(URL)
app = Dash(__name__)
sites = sorted(data["Launch Site"].unique())
app.layout = html.Div([
    html.H1("Falcon 9 landing outcomes"),
    dcc.Dropdown(id="site", options=[{"label":"All sites","value":"ALL"}] + [{"label":s,"value":s} for s in sites], value="ALL"),
    dcc.RangeSlider(id="payload", min=0, max=10000, step=500, value=[0,10000]),
    dcc.Graph(id="success-pie"), dcc.Graph(id="payload-scatter"),
])
@app.callback(Output("success-pie","figure"),Output("payload-scatter","figure"),Input("site","value"),Input("payload","value"))
def update(site, payload):
    filtered = data if site == "ALL" else data[data["Launch Site"] == site]
    filtered = filtered[filtered["Payload Mass (kg)"].between(*payload)]
    counts = filtered.assign(Outcome=filtered["class"].map({1:"Successful",0:"Unsuccessful"}))
    pie = px.pie(counts, names="Outcome", title="Landing outcome")
    scatter = px.scatter(counts, x="Payload Mass (kg)", y="Flight Number", color="Outcome", hover_data=["Launch Site","Booster Version Category"], title="Payload versus outcome")
    return pie, scatter
if __name__ == "__main__":
    app.run(debug=False)
