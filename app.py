#Imports
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd


# Test with 311 2012-Present 
data = pd.read_csv('311 2012-Present.csv')

# Create a Dash web application
app = dash.Dash(__name__)

#Coordinates of New Orleans to center map
new_orleans_coordinates = {'lat': 29.9511, 'lon': -90.0715}

# Layout of the Dash app
app.layout = html.Div([
    # Map component using dcc.Graph
    dcc.Graph(
        #Set id
        id='new-orleans-map',
        figure=px.scatter_mapbox(
            #Use 311 Data
            data,
            #Use Lat/Long in Data
            lat = 'latitude',
            lon = 'longitude',

            #Find correct projection and zoom to display city of New Orleans
            
            #?TO DO: Make this parameter toggalable by user to change map style
            mapbox_style='carto-positron',

            center = new_orleans_coordinates,

            #Title of data set being used
            title='311 Data 2012-Present',


        )
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)