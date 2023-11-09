import dash
from dash import html, dcc
from dash import dash_table
import pandas as pd
import plotly.express as px
from variable_descriptions import descriptions, file

# Read your data from an Excel file (absolute path)
df = pd.read_excel(file)

app = dash.Dash(__name__)

# Define a list of variables you want to create graphs for
variables = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness',
             'Key', 'Liveness', 'Loudness', 'Speechiness', 'Tempo',
             'Time_Signature', 'Valence']

# Create a dropdown for selecting the variable to display
variable_dropdown = dcc.Dropdown(
    id='variable-dropdown',
    options=[{'label': var, 'value': var} for var in variables],
    value=variables[0]  # Set the default variable to display
)

description_div = html.Div(id='description-div')

app.layout = html.Div([
    html.H1("Metadata: Top 10 Spotify Tracks Globally in '23 (n = 10,387)"),
    
    # Add the variable dropdown
    variable_dropdown,

     # Add a Div to hold the selected variable graph
    html.Div(id='variable-graph'),
    
    # Add the description_div
    description_div,
    
    # Add a Div to hold the selected variable graph
    html.Div(id='variable-graph'),
    
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns if i != 'uri'],
        data=df.to_dict('records'),
        style_table={
            'overflowX': 'auto',
            'border': '1px solid black',  # Add a black border to the table
        },
        style_header={
            'backgroundColor': 'grey',
            'color': 'white',
            'textAlign': 'center',
            'fontWeight': 'bold',  # Make header text bold
        },
        style_cell={
            'backgroundColor': 'grey',
            'color': 'white',
            'textAlign': 'center',
            'userSelect': 'none',  # Disable text selection in cells
            'border': '1px solid black',  # Add a black border to cells
            'whiteSpace': 'normal',  # Allow cell text to wrap
        },
        selected_columns=['Artist'],  # Only allow selecting cells in the 'Artist' column
        selected_rows=[],
        # Apply the styles to specific columns if needed
        style_data_conditional=[
            {
                'if': {'column_id': c},
                'backgroundColor': 'grey',  # Set the background color to grey for all cells
                'color': 'white',  # Set the text color to white for all cells
                'border': '1px solid black',  # Add a black border to cells
                'userSelect': 'none',  # Disable text selection in cells
            } for c in df.columns if c != 'uri'
        ],
    ),
])

@app.callback(
    dash.dependencies.Output('variable-graph', 'children'),
    dash.dependencies.Output('description-div', 'children'),
    dash.dependencies.Input('variable-dropdown', 'value')
)

def update_variable_graph(selected_variable):
    # Combine 'Artist' and 'Track' columns to create a new 'Artist:Track' column
    df['Artist:Track'] = df['Artist'] + ':' + df['Track']
    fig = px.bar(df, x='Artist:Track', y=selected_variable, title=selected_variable)
    text = f"Selected Variable: {selected_variable}"
    
    # Get the description for the selected variable from the descriptions dictionary
    description = descriptions.get(selected_variable, "")
    
    return dcc.Graph(figure=fig), [html.P(text), html.P(description)] 

if __name__ == '__main__':
    app.run_server(debug=True)
def update_variable_graph(selected_variable):
    # Combine 'Artist' and 'Track' columns to create a new 'Artist:Track' column
    df['Artist:Track'] = df['Artist'] + ':' + df['Track']
    fig = px.bar(df, x='Artist:Track', y=selected_variable, title=selected_variable)
    text = f"Selected Variable: {selected_variable}"
    
    # Get the description for the selected variable from the descriptions dictionary
    description = descriptions.get(selected_variable, "")
    
    return dcc.Graph(figure=fig), [html.P(text), html.P(description)] 

if __name__ == '__main__':
    app.run_server(debug=True)