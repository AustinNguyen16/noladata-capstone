#Imports
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback
import plotly.express as px
import pandas as pd


# Test with 311 2012-Present 
data = pd.read_csv('311 2012-Present.csv')
#print(data.columns)

# Create a Dash web application
app = dash.Dash(__name__)


#Coordinates of New Orleans to center map
new_orleans_coordinates = {'lat': 29.9511, 'lon': -90.0715}

#Columns to drop for table display
columns_to_drop = ['responsible_agency', 'geocoded_column']
data_display = data.drop(columns=columns_to_drop)

# Layout of the Dash app
app.layout = html.Div(children=[


    # Map component using dcc.Graph
    html.Div(
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
                title='311 Code Enforcement Data 2012-Present',
                zoom = 10
                #Hover Options
            


        ),
        style={'width': '100%', 'margin': '10px', 'marginTop': '50px', 'marginBottom':'10px', 'textAlign': 'center'})
    ),

    #Table Component
    html.Div(
        dash_table.DataTable(
            id='example-table',
            columns=[{'name': col, 'id': col} for col in data_display.columns],  # Define columns for the table
            data=data_display.to_dict('records'),  # Convert DataFrame to a format suitable for DataTable
            #style_table={'width': '1%', 'margin': '300px', 'marginTop': '20px'}  # Style for the table
            style_table={'width': '10%', 'marginTop': '10px' },

            
            filter_action = 'native', #This sets data filter to native dash type, which is a typed filter system, not menu type which may be desirable
                                      #Also need to specify type to enable gt, lt, eq comparison for numeric types
    ),
    style={'position': 'relative', 'width': '10%', 'height': '50vh'}
    ),

    html.Div(id="test-output")

], )

#Callbacks - these make the Dash app interactive by updating Outputs when Inputs change


#Attempt #3 of this callback: 




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True) 