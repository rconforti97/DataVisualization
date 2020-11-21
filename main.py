import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# It's actually correct, how they scored each area doesnt correlate to their total happiness they said

# Load CSV file from Datasets folder
df1 = pd.read_csv('2015.csv')
df2 = pd.read_csv('2016.csv')
df3 = pd.read_csv('2017.csv')
df4 = pd.read_csv('2018.csv')
df5 = pd.read_csv('2019.csv')

app = dash.Dash()

# Layout
app.layout = html.Div(children=[
    html.H1(children='World Happiness Dash',
            style={
                'textAlign': 'center',
                'color': '#ED553B'
            }
            ),
    html.Div('Web dashboard for Data Visualization of World Happiness', style={'textAlign': 'center'}),
    html.Div('World Happiness Based by Region', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(),
    # Start of Interactive Bar Chart Start
    html.H3('Interactive Bar chart'),
    html.Div('This bar chart represent the reported world happiness by region and year as well as '
             'what contributed to the score'),
    dcc.Graph(id='graph1', style={'background': '#544F4F'}),
    html.Div('Please select a region', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-region',
        options=[
            {'label': 'Australia and New Zealand', 'value': 'Australia and New Zealand'},
            {'label': 'Central and Eastern Europe', 'value': 'Central and Eastern Europe'},
            {'label': 'Eastern Asia', 'value': 'Eastern Asia'},
            {'label': 'Latin America and Caribbean', 'value': 'Latin America and Caribbean'},
            {'label': 'Middle East and Northern Africa', 'value': 'Middle East and Northern Africa'},
            {'label': 'North America', 'value': 'North America'},
            {'label': 'Southeastern Asia', 'value': 'Southeastern Asia'},
            {'label': 'Southern Asia', 'value': 'Southern Asia'},
            {'label': 'Sub-Saharan Africa', 'value': 'Sub-Saharan Africa'},
            {'label': 'Western Europe', 'value': 'Western Europe'}
        ],
        value='Central and Eastern Europe'
    ),
    # end of Interactive Bar Chart
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-region', "value")])
def update_figure(selected_region):
    stackbarchart_df = df1[df1['Region'] == selected_region]

    stackbarchart_df = stackbarchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    stackbarchart_df = stackbarchart_df.groupby(['Country']).agg(
        {'Happiness Score': 'sum', 'Economy (GDP per Capita)': 'sum', 'Family': 'sum',
         'Health (Life Expectancy)': 'sum', 'Freedom': 'sum', 'Trust (Government Corruption)': 'sum'}).reset_index()

    stackbarchart_df = stackbarchart_df.sort_values(by=['Happiness Score'], ascending=[False]).reset_index()

    trace1_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Economy (GDP per Capita)'],
                                  name='Economy',
                                  marker={'color': '#173F5F'})

    trace2_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Family'], name='Family',
                                  marker={'color': '#20639B'})

    trace3_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Health (Life Expectancy)'],
                                  name='Life Expectancy',
                                  marker={'color': '#3CAEA3'})

    trace4_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Freedom'], name='Freedom',
                                  marker={'color': '#F6D55C'})

    trace5_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Trust (Government Corruption)'],
                                  name='Trust in the Government',
                                  marker={'color': '#ED553B'})

    data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart, trace4_stackbarchart,
                          trace5_stackbarchart]

    return {'data': data_stackbarchart, 'layout': go.Layout(title='Happiness Scores in ' + selected_region,
                                                            xaxis={'title': 'Country'},
                                                            yaxis={'title': 'Happiness Levels'},
                                                            barmode='stack')}


if __name__ == '__main__':
    app.run_server()
