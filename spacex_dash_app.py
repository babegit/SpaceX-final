# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Label([
                                    "Enter Site",
                                dcc.Dropdown(
                                    id='site-dropdown', searchable=False,
                                    value='ALL', options=[
                                        {'label': 'All', 'value':'ALL'},
                                        {'label': 'CCAFS SLC 40', 'value':'CCAFS SLC 40'},
                                        {'label': 'KSC LC 39A', 'value':'KSC LC 39A'},
                                        {'label': 'VAFB SLC 4E', 'value':'VAFB SLC 4E'},
                                        {'label': 'CCAFS LC 40', 'value':'CCAFS LC 40'},
                                    ]),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0:'0', 1000:'1000', 2000:'2000', 4000:'4000', 6000:'6000', 8000:'8000', 10000:'10000'},
                                    value=[min_payload, max_payload])
                                ]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
])
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def get_pie_chart(site_dropdown):
    if site_dropdown =='ALL':
        df2 = spacex_df.groupby(['Launch Site'])['Class'].sum().to_frame()
        df2 = df2.reset_index()
        fig = px.pie(df2, values='class', names='Launch Site',
        title='Total Launch Success')
        return fig
    else:
            df3 = spacex_df[spacex_df['Launch Site']==site-dropdown]['class'].value_counts().to_frame()
            df3["name"]=["Failure", "Success"]
            fig = px.pie(df3, values='class', names='name', title='Total Success  Launches'+ site-dropdown)
        return fig
        )
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
    Input("payload-slider", "value")]
)
def scatter-chart(site_dropdown, payload_slider):
    df4 = spacex_df[spacex_df['Payload Mass(kg)'].between(payload[0], payload[1])]
    if site_dropdown =='ALL':
        fig = px.scatter(df4, x='Payload Mass(kg)', y='Class',
        color='Booster Version Category',
        title="Payload Mass Success Count")
        return fig
    else:
        fig=px.scatter(df4[df4['Launch Site']==site_dropdown], x='Payload Mass(kg)',
        y='Class', color='Booster Version Category',
        title="Success Payload Mass by Site{site_dropdown}")
        return fig
        )
# Run the app
if __name__ == '__main__':
    app.run_server()
