#Imports
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback, callback_context
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
    mycursor.execute("SELECT * FROM blightdata")
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
             'data_source',
             'request_status',
             'objectid',
             'casefiled',
             'o_c',
             'latitude',
             'longitude']


#Set data to our df from server
data = df[data_cols]

#Dictionary mapping to rename columns to more readable format 
new_column_names = {
    'final_address':'Address',
    'data_source': 'Source',
    'request_status':'Request Status',
    'objectid':'Object ID',
    'casefiled':'Case Filed Date',
    'o_c':'Open/Closed',
    'latitude':'Latitude',
    'longitude':'Longitude'
}

data = data.rename(columns=new_column_names)
data = data.fillna('n/a')

# Create a Dash web application
app = dash.Dash(__name__, external_stylesheets=['/assets/styles.css'])

#Global Vars
#Coordinates of New Orleans to center map
new_orleans_coordinates = {'lat': 29.9511, 'lon': -90.0715}

#Columns to drop for table display
columns_to_drop = ['geocoded_column', 'geoaddress']
data_display = data #.drop(columns=columns_to_drop)


#Quick start modal
quick_start_modal = html.Div(
    id='quick-start-modal',
    className='modal',
    children=[
        html.Div(
            className='modal-content',
            children=[
                html.Span(className='close', id='quick-start-close', children='×'),
                html.H2('Quick Start Guide'),
                html.P('This is the quick start guide. Add your instructions here.')
            ]
        )
    ]
)

#Quadrant 1 subquadrant divs
total_observations = data.shape[0]
subquadrant_1_content = html.Div(children=[
    html.Img(src='/assets/house-png-193.png', style= {'width':'10%', 'height':'10%', 'display':'inline-block'}),
    html.H3('Total Properties Tracked'),
    html.H3(f'{total_observations}')
    ],
    style={'text-align':'center', 'border':'2px solid #000000', 'border-radius':'10px', 'padding-top':'20px'}
    )

pending_311_complaints = data[data["Request Status"] == "Pending"].shape[0]
subquadrant_2_content = html.Div(children=[
    html.Img(src='/assets/phone-clipart.png', style= {'width':'10%', 'height':'10%', 'display':'inline-block', }),
    html.H3('Pending 311 Complaints'),
    html.H3(f'{pending_311_complaints}')
    ],
    style={'text-align':'center', 'border':'2px solid #000000', 'border-radius':'10px', 'padding-top':'20px'}
    )
subquadrant_3_content = html.Div(children=[
    html.Img(src='/assets/gavel-clipart.png', style= {'width':'10%', 'height':'10%', 'display':'inline-block'}),
    html.H3('Oldest Code Enforcement Case'),
    html.H3('3639 - 3641 Republic St (01/03/2014)')
    ],
    style={'text-align':'center', 'border':'2px solid #000000', 'border-radius':'10px', 'padding-top':'20px'}
    )
subquadrant_4_content = html.Div(children=[
    html.Img(src='/assets/broken-house-clipart.png', style= {'width':'10%', 'height':'10%', 'display':'inline-block'}),
    html.H3('Vacant Properties'),
    html.H3('242')
    ],
    style={'text-align':'center', 'border':'2px solid #000000', 'border-radius':'10px', 'padding-top':'10px'}
    )

#Main quadrant divs
quadrant_1_content = html.Div(children=[
    html.H2('Welcome to BlightWatch NOLA', style= {'font-family':'Georgia, serif', 'color':'black'}),
    html.P('This app unifies publicly available 311 call, Code Enforcement, and USPS Vacancy data' + 
           ' to help users track blighted properties in New Orleans. For more information about our sources,' +
            ' click the \'Data Sources\' button in the menu bar. To get started, use our Quick Start Guide.',
           style= {'font-family':'Georgia, serif', 'color':'black'}),
    html.Div(
    style={
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr',  # Two columns
        'gridTemplateRows': '1fr 1fr',     # Two rows
        'height': '40vh',                 # Full height of the viewport
        'gap': '10px'                       # Gap between grid items
    },
    children=[
        
        html.Div(subquadrant_1_content, style={'gridColumn': '1', 'gridRow': '1'}),
        html.Div(subquadrant_2_content, style={'gridColumn': '2', 'gridRow': '1'}),
        html.Div(subquadrant_3_content, style={'gridColumn': '1', 'gridRow': '2'}),
        html.Div(subquadrant_4_content, style={'gridColumn': '2', 'gridRow': '2'})
    ]
)
    ],
    style={'paddingLeft':'10px'}
)
quadrant_2_content = html.Div(

        dcc.Graph(
        #Set id
            id='new-orleans-map',
            figure=px.scatter_mapbox(
                #Use df from database
                data,
                #Use Lat/Long in Data
                lat = 'Latitude',
                lon = 'Longitude',

                #Find correct projection and zoom to display city of New Orleans
            
                #?TO DO: Make this parameter toggalable by user to change map style
                mapbox_style='carto-positron',

                center = new_orleans_coordinates,

                #Title of data set being used
                title='Tracked Properties',
                zoom = 10,
                
                #Hover Options
                color='Source',
                color_discrete_map= {'311 Calls': 'blue', 'Code Enforcement': 'red'},
                hover_name= 'Address',
                hover_data= {'Request Status':True, 'Source':True, 'Object ID':True, 'Case Filed Date':True, 
                             'Open/Closed':True,} #Controls columns that display on hover
            


        ), 
        style={'width': '50vw', 
               'margin': '10px', 
               'marginTop': '0px', 
               'marginBottom':'0px', 
               'textAlign': 'center',
               'padding-bottom': '0px',
               'left':'15%',
               'backgroundColor':'gray'}) #end graph
    ), #end map div

source_counts = data.groupby('Source').size().reset_index(name='counts')
fig = px.pie(source_counts, names='Source', values='counts', title='Pie Chart')
fig.update_layout(title='Breakdown of Data Sources')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
quadrant_3_content = html.Div(children=[
    #Add Pie Graph of 311 vs Code Enf
    html.Div(
        dcc.Graph(
            id="pie-graph",
            figure=fig,
            

            ),
         #style={'background-color': 'LightSlateGray'}# Graph div Style
    ),
    
    ],
    style={'width':'45vw', 'height':'45vh', 'margin':'10px'} #Q3 Div style
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

                        style_cell_conditional=[  # Set width for specific columns
                            {'if': {'column_id': 'Address'}, 'width': '30px'},
       
                            ],
                        

                        #tooltip specs
                        tooltip_header={
                        "Address": "The address of the property",
                        "Source": "The data source of the tracked property. Read more about the data sources in the \'About\' section.",
                        "Request Status": "311 request status of property",
                        "Object ID": "Code Enforcement: The case identification number",
                        "Case Filed Date": "Code Enforcement: The date the case was filed",
                        "Open/Closed": "Code Enforcement: Whether the case is open or closed",
                        "Latitude": "The latitude coordinate of the property",
                        "Longitude": "The longitude coordinate \n of the property"
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
            'display': 'inline-block', 'maxHeight': '250px', 'overflowY': 'scroll', 'paddingLeft': '20px', #Controls for scroll frame
            #'backgroundColor':'gray'
            }   
        )#end table div
    ]
) #end table container div


# Layout of the Dash app
app.layout = html.Div(children=[

    #Header div
    html.Div(children=[
            html.H2('BlightWatch NOLA', style= {'font-family':' Georgia, serif', 'color':'white', 'display':'inline-block',
                                                'margin-left':'2px'}),
            html.H4('Home', style={'font-family':' Georgia, serif', 'color':'white', 'display':'inline-block',
                                           'margin-left':'40px'}),
            html.H4('Data Sources', style={'font-family':' Georgia, serif', 'color':'white', 'display':'inline-block',
                                           'margin-left':'20px'}),
            html.H4('About', style={'font-family':' Georgia, serif', 'color':'white', 'display':'inline-block',
                                           'margin-left':'20px'})
            ],
            style={'backgroundColor':'black', 'padding':'0px', 'border':'0px', 'margin':'0px'}
        ),

    #Quick Start modal div, commented out for now because it isn't working right
    #html.Button('Open Quick Start Guide', id='quick-start-open'),
    #quick_start_modal,


    #4-quadrants div
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

# Callback to toggle the display of the quick start guide modal
@app.callback(
    Output('quick-start-modal', 'style'),
    [Input('quick-start-open', 'n_clicks'),
     Input('quick-start-close', 'n_clicks')],
    [State('quick-start-modal', 'style')]
)
def toggle_modal(open_clicks, close_clicks, style):
    if open_clicks or close_clicks:
        if 'none' in style.get('display', 'none'):
            style['display'] = 'block'
        else:
            style['display'] = 'none'
    return style



# Run the app
if __name__ == '__main__':
    app.run_server(debug=False) 