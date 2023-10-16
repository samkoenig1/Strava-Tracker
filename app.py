import pandas as pd
from pandas import json_normalize

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import calendar
import login as login

#pull auth_url
auth_url = 'https://www.strava.com/oauth/token'
#define activies_url per
activities_url = 'https://www.strava.com/api/v3/athlete/activities'


#pull identification keys from the login.py file
payload = {
    'client_id': f'{login.client_id}',
    'client_secret': f'{login.client_secret}',
    'refresh_token': f'{login.refresh_token}',
    'grant_type': 'refresh_token',
    'f': 'json'
}

#name that we are requesting a toke
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

header = {'Authorization': 'Bearer ' + access_token}
page =1
#request data from the activieies url. Strava's API only allows 200 per page. Leaving the page value variable so we can loop through in the future
get_strava = requests.get(activities_url, headers=header, params={'per_page': 200, 'page': f'{page}'}).json()

#take the json data and normalize it as a pandas dataframe
activities = json_normalize(get_strava)
# The Strava API only supports 200 results per page. This function loops through each page until new_results is empty.

#convert km --> miles
activities.distance = activities.distance / 1609
#convert km/hr --> mph
activities.average_speed = activities.average_speed * 2.237

#convert start date into string month
activities['start_date_month'] = pd.DatetimeIndex(activities['start_date_local']).month

#convert start date into year
activities['start_date_year'] = pd.DatetimeIndex(activities['start_date_local']).year
activities['year_month'] = activities.start_date_month.map(str) + '/' + activities.start_date_year.map(str)

#group actiities by number of actiities, total distance, and average speed
activities = activities.groupby('year_month').agg({'year_month':'min','id':'count', 'distance':'sum','average_speed': 'mean', 'start_date_local':'min'})

#rename columns
activities.columns = ['year_month','number_of_activities','total_distance','average_speed','start_date']

#change format back into date format
activities['year_month'] = pd.to_datetime(activities['year_month'], format ='%m/%Y')
activities['avg_activities_month'] = activities['total_distance'] /  activities['number_of_activities']
#round values to 1
activities = activities.round(1)

##Beginning of Dash app##
app = Dash(__name__)
app = Dash(external_stylesheets=[dbc.themes.CERULEAN])

#Create app layout
app.layout = html.Div([
# Title of the App
    html.H1('Strava Activities Over Time',
        style = {'margin-left':'25px'}),
# Create dropdown for metrics of interest
    dcc.Dropdown(
        id="dropdown",
        options=["Total Distance (Miles)", "# Activities", "Average Speed", "Avg Miles / Run"],
        value= "Total Distance (Miles)",
        style={
                'width': '50%',
                'margin-left': '50px'
            }
        ),
    dcc.Graph(id="graph"),
])

#add dropdown underneath title
@app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value"))

#Create dynamic chart
def update_bar_chart(dropdown):
    df = activities # replace with your own data source

#Based on the dropdown adjust the Y value of interest between Average speed, average distance, # activities, and avg miles / run
    if dropdown == "Total Distance (Miles)":
          fig = px.bar(df, x="year_month",
          y= "total_distance",
          color = "total_distance",
          text_auto = True,
          labels = {'year_month': 'Date', 'total_distance': 'Total Distance (Miles)'}, )
    elif dropdown == "# Activities":
          fig = px.bar(df, x="year_month",
          y= "number_of_activities",
          color = "number_of_activities",
          text_auto = True,
          labels = {'year_month': 'Date', 'number_of_activities': '# Activities'})
    elif dropdown == "Average Speed":
          fig = px.bar(df, x="year_month",
          y= "average_speed",
          color = "average_speed",
          text_auto = True,
          labels = {'year_month': 'Date', 'average_speed': 'Average Speed'})
    elif dropdown == "Avg Miles / Run":
          fig = px.bar(df, x="year_month",
          y= "avg_activities_month",
          color = "avg_activities_month",
          text_auto = True,
          labels = {'year_month': 'Date', 'avg_activities_month': 'Average Miles / Run'})
    fig.update_xaxes(tickangle=45)
    return fig

#run app on the server
app.run_server(debug=True)
