import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

# Global variables
tabtitle = 'Drinks world!'
color1='teal'
color2='lightblue'
color3='crimson'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/plotly-dash-apps/304-titanic-dropdown'


# Load data for anlysis
# https://github.com/austinlasseter/plotly_dash_tutorial/blob/master/00%20resources/titanic.csv
url = "https://raw.git.generalassemb.ly/intuit-ds-15/05-cleaning-combining-data/master/data/drinks.csv?token=AAAKG5FAE42EI3LMYHV2YIDCHUFWI"
df = pd.read_csv(url)
df['Alcohol Level'] = pd.cut(
    x=df['total_litres_of_pure_alcohol'],
    bins=[0.0, 5.0, 10.0, 100.0],
    labels=['Low', 'Medium', 'High'])
df['Alcohol Level'] = df['Alcohol Level'].fillna('Low')
df.loc[df['country'].isna(), 'continent'] = 'NA'
df['beer_servings'] = df['beer_servings'].fillna(0.0)
print(df)

# df['Female'] = df['Sex'].map({'male': 0, 'female': 1})
# df['Cabin Class'] = df['Pclass'].map({1: 'first', 2: 'second', 3: 'third'})
variables_list = [
    'beer_servings',
    'spirit_servings',
    'wine_servings',
    'total_litres_of_pure_alcohol']

# app server config
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

# app component layout
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]),
    html.Br(),
    dcc.Graph(id='output1'),
    html.Br(),
    dcc.Graph(id='output2'),
    # html.Br(),
    # dcc.Graph(id='scatter1'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])

# callback
@app.callback(
    Output('output1', 'figure'),
    [Input('dropdown', 'value')])
def display_value(option):
    grouped_mean = df.groupby(['Alcohol Level', 'continent'])[option].mean()
    results = pd.DataFrame(grouped_mean)
    print(results)

    # Create a grouped bar chart
    data1 = go.Bar(
        x=results.loc['Low'].index,
        y=results.loc['Low'][option],
        name='Low Alcohol',
        marker=dict(color=color1),
        text=round(results.loc['Low'][option],1),
        textposition='auto')

    data2 = go.Bar(
        x=results.loc['Medium'].index,
        y=results.loc['Medium'][option],
        name='Medium Alcohol',
        marker=dict(color=color2),
        text=round(results.loc['Medium'][option],1),
        textposition='auto')

    data3 = go.Bar(
        x=results.loc['High'].index,
        y=results.loc['High'][option],
        name='High Alcohol',
        marker=dict(color=color3),
        text=round(results.loc['High'][option],1),
        textposition='auto')

    layout = go.Layout(
        title='Drink consumption by continent bar chart',
        xaxis=dict(title='Continent'), # x-axis label
        yaxis=dict(title=str(option)),) # y-axis label

    return go.Figure(data=[data1, data2, data3], layout=layout)
    #return go.Figure(data=[data1], layout=layout)

# callback
@app.callback(
    Output('output2', 'figure'),
    [Input('dropdown', 'value')])
def display_value(option):
    grouped_mean = df.groupby(['Alcohol Level', 'continent'])[option].mean()
    results = pd.DataFrame(grouped_mean)
    rows = 1
    cols = 3
    specs = [[{'type': 'domain'}] * cols] * rows
    fig = make_subplots(
        rows=1,
        cols=3,
        specs=specs,)

    # Create a grouped bar chart
    fig.add_trace(go.Pie(
        labels=results.loc['Low'].index,
        values=results.loc['Low'][option],
        title="Low Alcohol",
        hoverinfo="label+percent+name",
        ), 1, 1)

    fig.add_trace(go.Pie(
        labels=results.loc['Medium'].index,
        values=results.loc['Medium'][option],
        title="Medium Alcohol",
        hoverinfo="label+percent+name"), 1, 2)

    fig.add_trace(go.Pie(
        labels=results.loc['High'].index,
        values=results.loc['High'][option],
        title="High Alcohol",
        hoverinfo="label+percent+name"), 1, 3)

    fig.update_traces(hole=0.7, hoverinfo='label+percent+name')

    layout = go.Layout(
        title='Drink consumption by continent PIE chart',
        xaxis=dict(title='Continent'),
        yaxis=dict(title=str(option)),
        annotations=[
            dict(text='Low', x=0.12, y=0.6, font_size=100, showarrow=False),
            dict(text='Medium', x=0.15, y=0.6, font_size=20, showarrow=False),
            dict(text='High', x=0.18, y=0.6, font_size=20, showarrow=False)])

    return go.Figure(data=fig, layout=layout)


# # callback
# @app.callback(
#     Output('scatter1', 'figure'),
#     [Input('dropdown', 'value')])
# def display_value(option):
#     data=go.Scatter(
#         x=df['country'],
#         y=df['total_litres_of_pure_alcohol'],
#         mode='markers',
#         marker_color=df['total_litres_of_pure_alcohol'],
#         marker_size=df['total_litres_of_pure_alcohol'],
#         text=df['country']) # hover text goes here
#     layout = go.Layout(
#         title='Drink consumption by continent scatter chart',
#     )
#     return go.Figure(data=data, layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True)
