
#MAP DIV
    html.Div(
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
        style={'width': '100%', 
               'margin': '10px', 
               'marginTop': '0px', 
               'marginBottom':'0px', 
               'textAlign': 'center',
               'padding-bottom': '0px'
               }) #end graph
    ), #end map div



#Table Container Div

    html.Div(
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
           'width': '60%', 
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


#Quick Start Guide Div

html.Div(children=[
    html.H2('Welcome to Blightwatch NOLA', style= {'font-family':'Georgia, serif',}),
    html.P('This app unifies publicly available data to help users understand blighted properties in New Orleans.'),
    html.H2('Quick Start Guide:'),
    html.Ul([
        html.Li('Map tools will appear in the top-right when you hover over the map. Use the \'Box Select\' or'  +
                ' the \'Lasso Select\' tool to highlight a specific area of the city. Double click to clear your selection.'),
        html.Li('The table can also be used to filter the data. Search for a specific property or street name by typing'+
                 ' in the \'filter data...\' box under the \'Address\' column header.' + 
                 ' To reset the table, backspace the entry in \'filter data...\' and hit enter.'),
        html.Li('You can also filter the other text columns by typing in the \'filter data...\' below the column header.' +
                ' Numeric columns support direct search of values (i.e. -90.132), as well as the use of' +
                ' greater than (>), less than (<), greater than or equal to (>=), and less than or equal to (<=).'),
        html.Li('The table also supports multiple column filters at once, simply type the filter you want for each column in their respective'+ 
                ' \'filter data...\' box, and the table will display all the properties that match the filtered qualities.')
    ]
        
    )
    ]
)