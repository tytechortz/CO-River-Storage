import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
import time
import requests
import csv 
from datetime import datetime, date, timedelta
# from data import powell_df

today = time.strftime("%Y-%m-%d")


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

# powell_data = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=509&before=' + today + '&after=2000-01-01&filename=Lake%20Powell%20Glen%20Canyon%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20'

# with requests.Session() as s:

#     powell_download = s.get(powell_data)
    
#     powell_decoded_content = powell_download.content.decode('utf-8')

#     crp = csv.reader(powell_decoded_content.splitlines(), delimiter=',')
    
    
#     for i in range(9): next(crp)
#     df_powell_water = pd.DataFrame(crp)
    
#     df_powell_water = df_powell_water.drop(df_powell_water.columns[[1,3,4,5]], axis=1)
#     df_powell_water.columns = ["Site", "Value", "Date"]

#     df_powell_water = df_powell_water[1:]
    
#     df_powell_water['power level'] = 6124000

#     df_powell_water = df_powell_water.set_index("Date")
#     df_powell_water = df_powell_water.sort_index()
    
# powell_df = df_powell_water.drop(df_powell_water.index[0])

# print(powell_df.tail(50))


# powell_fig = go.Figure()
# powell_fig.add_trace(go.Scatter(
#     y = powell_df['Value'],
#     x = powell_df.index,
#     name='Water Level',
#     mode='lines+markers'
# ))
# powell_fig.add_trace(go.Scatter(
#     y = powell_df['power level'],
#     x = powell_df.index,
#     name = 'Power level'
# )),

# powell_fig.update_layout(
#     height =400,
#     title = 'Lake Powell',
#     yaxis = {'title':'Volume (AF)'},
#     paper_bgcolor="#1f2630",
#     plot_bgcolor="#1f2630",
#     font=dict(color="#2cfec1"),
# )

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
            className='four columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='mead-levels',
            ),
        ],
            className='four columns'
        ),
        html.Div([
            dcc.Graph(
                # figure=powell_fig,
                id='powell-levels',
            ),
        ],
            className='four columns'
        ),

    ],
        className='row'
    ),
    html.Div(id='powell-water-data', style={'display': 'none'}),
    html.Div(id='mead-water-data', style={'display': 'none'}),
])


@app.callback([
    Output('powell-water-data', 'children'),
    Output('mead-water-data', 'children')],
    [Input('lake', 'value')])
def clean_powell_data(lake):
    
    powell_data = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=509&before=' + today + '&after=1999-12-29&filename=Lake%20Powell%20Glen%20Canyon%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20'

    mead_data = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=6124&before=' + today + '&after=1999-12-30&filename=Lake%20Mead%20Hoover%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(1937-05-28%20-%202020-11-30)&order=ASC'

    # if lake == 'lakepowell':

    with requests.Session() as s:

        powell_download = s.get(powell_data)
        
        powell_decoded_content = powell_download.content.decode('utf-8')
    
        crp = csv.reader(powell_decoded_content.splitlines(), delimiter=',')
        
        
        for i in range(9): next(crp)
        df_powell_water = pd.DataFrame(crp)
        
        df_powell_water = df_powell_water.drop(df_powell_water.columns[[1,3,4,5]], axis=1)
        df_powell_water.columns = ["Site", "Value", "Date"]
    
        df_powell_water = df_powell_water[1:]
        
        df_powell_water['power level'] = 6124000

        df_powell_water = df_powell_water.set_index("Date")
        df_powell_water = df_powell_water.sort_index()
    
    powell_df = df_powell_water.drop(df_powell_water.index[0])

    with requests.Session() as s:
        mead_download = s.get(mead_data)

        mead_decoded_content = mead_download.content.decode('utf-8')

        crm = csv.reader(mead_decoded_content.splitlines(), delimiter=',')

        for i in range(9): next(crm)
        df_mead_water = pd.DataFrame(crm)
        df_mead_water = df_mead_water.drop(df_mead_water.columns[[1,3,4,5]], axis=1)
        df_mead_water.columns = ["Site", "Value", "Date"]
    
        df_mead_water['1090'] = 10857000
        df_mead_water['1075'] = 9601000
        df_mead_water['1050'] = 7683000
        df_mead_water['1025'] = 5981000

        df_mead_water = df_mead_water.set_index("Date")
        df_mead_water = df_mead_water.sort_index()
        
    mead_df = df_mead_water.drop(df_mead_water.index[0])

    print(mead_df.head())
    print(powell_df.head())

           
    start_date = date(1963, 6, 29)
    date_now = date.today()
    delta = date_now - start_date
    
    days = delta.days
    df_mead_water = mead_df[9527:]
    
    df_total = pd.merge(df_mead_water, df_powell_water, how='inner', left_index=True, right_index=True)

    df_total.rename(columns={'Date_x':'Date'}, inplace=True)
    
    df_total['Value_x'] = df_total['Value_x'].astype(int)
    df_total['Value_y'] = df_total['Value_y'].astype(int)
    df_total['Value'] = df_total['Value_x'] + df_total['Value_y']
    
    # combo_df = df_total.drop(df_total.index[0])
    # print(combo_df.head())

    return powell_df.to_json(), mead_df.to_json()

def powell_level():
    powell_traces = []
    powell_data = powell_df.sort_index()
    powell_traces.append(go.Scatter(
        y = powell_df['Value'],
        x = powell_df.index,
        name='Water Level'
        )),
    powell_traces.append(go.Scatter(
        y = powell_df['power level'],
        x = powell_df.index,
        name = 'Power level'
        )),
    layout = go.Layout(
        height =400,
        title = title,
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )
    return {'data': powell_traces, 'layout': layout}


@app.callback([
    Output('powell-levels', 'figure'),
    Output('mead-levels', 'figure')],
    [Input('lake', 'value'),
    Input('powell-water-data', 'children'),
    Input('mead-water-data', 'children')])
def lake_graph(lake, powell_data, mead_data):
    powell_df = pd.read_json(powell_data)
    mead_df = pd.read_json(mead_data)

    mead_traces = []
    powell_traces = []
    # if lake == 'hdmlc':
      
    data = mead_df.sort_index()
    # title = 'Lake Mead'
    for column in mead_df.columns[1:]:
        mead_traces.append(go.Scatter(
            y = mead_df[column],
            x = mead_df.index,
            name = column
        ))
    # elif lake == 'lakepowell':
      
    data = powell_df.sort_index()
    # title = 'Lake Powell'
    powell_traces.append(go.Scatter(
        y = powell_df['Value'],
        x = powell_df.index,
        name='Water Level'
    )),
    powell_traces.append(go.Scatter(
        y = powell_df['power level'],
        x = powell_df.index,
        name = 'Power level'
    )),
    # elif lake == 'combo':
    #     title = 'Lake Powell and Lake Mead'
    #     traces.append(go.Scatter(
    #         y = combo_df['Value'],
    #         x = combo_df.index,
    #         name='Water Level'
    #     )),

    mead_layout = go.Layout(
        height =400,
        title = 'Lake Mead',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    powell_layout = go.Layout(
        height =400,
        title = 'Lake Powell',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )
    return {'data': mead_traces, 'layout': mead_layout}, {'data': powell_traces, 'layout': powell_layout}

if __name__ == '__main__':
    app.run_server(debug=True)