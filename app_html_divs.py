
#MAP DIV
html.Div([
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
            zoom = 10
            #Hover Options
            


        )
    )
], style={'width': '50%', 'margin': '300px', 'marginTop': '50px', 'textAlign': 'center'}
)