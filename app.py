import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

app.layout = html.Div([
    html.Div([
        html.H2(
            'Colorado River Water Storage',
            className='twelve columns',
            style={'text-align': 'center'}
        ),
    ],
        className='row'
    ),
    html.Div([
        dcc.Dropdown(
            id='lake',
            options=[
                {'label': 'Powell', 'value': 'lakepowell'},
                {'label': 'Mead', 'value': 'hdmlc'},
            ],
            value='lakepowell'
        )
    ],
        className='row'
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)