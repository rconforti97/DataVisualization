import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

fig = go.Figure()

# Load CSV file from Datasets folder
df1 = pd.read_csv('2018.csv')

# Cloropeth
fig = go.Figure(data=go.Choropleth(
    locationmode='country names',
    locations=df1['Country'],
    z = df1['Score'],
    text = df1['Country'],
    colorscale = 'Greens',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='Happiness Score',
))
# Cloropeth

fig.update_layout(
    title_text='2018 World Happiness',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations=[dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
            CIA World Factbook</a>',
        showarrow=False
    )]
)
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
    dcc.Graph(id='graph1', figure=fig, style={'background': '#544F4F'}),
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
    dcc.Graph(id="Coloropeth",figure=fig)
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-region', "value")])
def update_figure(selected_region):
    stackbarchart_df = df1[df1['Region'] == selected_region]

    stackbarchart_df = stackbarchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    stackbarchart_df = stackbarchart_df.groupby(['Country']).agg(
        {'Overall rank': 'sum', 'GDP per capita': 'sum', 'Social support': 'sum',
         'Healthy life expectancy': 'sum', 'Freedom to make life choices': 'sum', 'Generosity': 'sum',
         'Perceptions of corruption': 'sum'}).reset_index()

    stackbarchart_df = stackbarchart_df.sort_values(by=['Overall rank'], ascending=[False]).reset_index()

    trace1_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['GDP per capita'],
                                  name='Economy', marker={'color': '#173F5F'})

    trace2_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Social support'],
                                  name='Social support', marker={'color': '#20639B'})

    trace3_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Healthy life expectancy'],
                                  name='Healthy life expectancy', marker={'color': '#3CAEA3'})

    trace4_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Freedom to make life choices'],
                                  name='Freedom', marker={'color': '#F6D55C'})

    trace5_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Generosity'],
                                  name='Generosity',
                                  marker={'color': '#ED553B'})

    # Change this color....
    trace6_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Perceptions of corruption'],
                                  name='Perceptions of corruption', marker={'color': '#ED553B'})

    data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart, trace4_stackbarchart,
                          trace5_stackbarchart, trace6_stackbarchart]

    return {'data': data_stackbarchart, 'layout': go.Layout(title='Happiness Scores in ' + selected_region,
                                                            xaxis={'title': 'Country'},
                                                            yaxis={'title': 'Happiness Overall'},
                                                            barmode='stack')}



if __name__ == '__main__':
    app.run_server()
fig.show()