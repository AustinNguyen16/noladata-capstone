#Imports
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback
import plotly.express as px
import pandas as pd
import mysql.connector


#Database connection for local editing

host = "sql5.freesqldatabase.com" 
user = "sql5680691" 
password = "g4fgFKv83C" 
database = "sql5680691" 
port = 3306 

#Database connection for production
'''host = "jtmcdermott9.mysql.pythonanywhere-services.com"
user = "jtmcdermott9"
password = "Ihatemysql123"
database = "jtmcdermott9$capstone"
port = 3306'''

connection = mysql.connector.connect(
                                    host=host,     
                                    user=user,     
                                    password=password,     
                                    database=database,     
                                    port=port ) 

mycursor = connection.cursor()


#Put database read in try/except block for safety

try:
    mycursor.execute("SELECT * FROM df_blight3")
    rows = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]

    df = pd.DataFrame(rows, columns=columns)
    

except:
    print("Error loading data")
else:
    print("Data loaded successfully into dataframe")
finally:
    print("End of try/except")


#Reorder column names
data_cols = ['final_address',
             'request_status',
             'objectid',
             'casefiled',
             'o_c',
             'latitude',
             'longitude']


#Set data to our df from server
data = df[data_cols]



# Create a Dash web application
app = dash.Dash(__name__)

#Global Vars
#Coordinates of New Orleans to center map
new_orleans_coordinates = {'lat': 29.9511, 'lon': -90.0715}

#Columns to drop for table display
columns_to_drop = ['geocoded_column', 'geoaddress']
data_display = data #.drop(columns=columns_to_drop)


quadrant_1_content = html.Div(
    html.H1('Test 1')
)
quadrant_2_content = html.Div(

        dcc.Graph(
        #Set id
            id='new-orleans-map',
            figure=px.scatter_mapbox(
                #Use df from database
                data,
                #Use Lat/Long in Data
                lat = 'latitude',
                lon = 'longitude',

                #Find correct projection and zoom to display city of New Orleans
            
                #?TO DO: Make this parameter toggalable by user to change map style
                mapbox_style='carto-positron',

                center = new_orleans_coordinates,

                #Title of data set being used
                title='New Orleans Blighted Properties',
                zoom = 10
                #Hover Options
            


        ),
        style={'width': '50vw', 
               'margin': '10px', 
               'marginTop': '0px', 
               'marginBottom':'0px', 
               'textAlign': 'center',
               'padding-bottom': '0px'
               }) #end graph
    ), #end map div

quadrant_3_content = html.Div(
    html.H1('Test 3')
)
quadrant_4_content = html.Div(
        style={'textAlign': 'center', 'left': '60%'},  # Center align content inside this div
        children=[
            html.Div(
                          
                children=[
      

                    #table component
                    dash_table.DataTable(
                        id='nola-blight-table',
                        columns=[{'name': col, 'id': col} for col in data_display.columns],  # Define columns for the table
                        data=data_display.to_dict('records'),  # Convert DataFrame to a format suitable for DataTable
                        style_table={'width': '10%', 'marginTop': '10px'},  # Style for the table
                        filter_action='native',  # Set data filter to native dash type
                        filter_query='',  # Initial filter query

                        #tooltip specs
                        tooltip_header={
                        "final_address": "The address of the property",
                        "request_status": "311 request status of property",
                        "objectid": "[INSERT]",
                        "casefiled": "[INSERT]",
                        "o_c": "Whether the case is open or closed",
                        "latitude": "the latitude coordinate of the property",
                        "longitude": "the longitude coordinate of the property"
                    },
                    tooltip_duration=None
        ), #end table
        
    ],
    style={'position': 'relative', 
           'width': '50vw', 
           'height': '50vh',
           'textAlign': 'center',
           'display': 'flex',  # Ensures children are displayed as flex items
            'flexDirection': 'column',
            'left': '0%', #This moves the table to the center
            'display': 'inline-block', 'maxHeight': '250px', 'overflowY': 'scroll', 'paddingLeft': '20px' #Controls for scroll frame
            }   
        )#end table div
    ]
) #end table container div

# Layout of the Dash app
app.layout = html.Div(children=[

    html.Div(
    style={
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr',  # Two columns
        'gridTemplateRows': '1fr 1fr',     # Two rows
        'height': '100vh',                 # Full height of the viewport
        'gap': '10px'                       # Gap between grid items
    },
    children=[
        html.Div(quadrant_1_content, style={'gridColumn': '1', 'gridRow': '1'}),
        html.Div(quadrant_2_content, style={'gridColumn': '2', 'gridRow': '1'}),
        html.Div(quadrant_3_content, style={'gridColumn': '1', 'gridRow': '2'}),
        html.Div(quadrant_4_content, style={'gridColumn': '2', 'gridRow': '2'})
    ]
)



    
  
    
], )#end of layout div

#Callbacks - these make the Dash app interactive by updating Outputs when Inputs change

#Map -> Table - this actually works!!
@callback(
        Output('nola-blight-table', 'data'),
        Input('new-orleans-map', 'selectedData')
)
def update_table(selectedData):
    if selectedData is None:
        return data.to_dict('records')
    
    # Filter data based on selected points on the map
    selected_points = [point['pointIndex'] for point in selectedData['points']]
    filtered_df = data.iloc[selected_points]
    
    return filtered_df.to_dict('records')

#Table -> Map 
@callback(
    Output('new-orleans-map', 'figure'),
    Input('nola-blight-table', 'filter_query'),
    #State('nola-blight-table', 'data')
)

def update_map(filter_query):
    filtered_data = data.query(filter_query)

    figure = px.scatter_mapbox(
        filtered_data,
        lat='latitude',
        lon='longitude',
        mapbox_style='carto-positron',
        center=new_orleans_coordinates,
        title='new-orleans-map',
        zoom=10
    )

    return figure



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True) 