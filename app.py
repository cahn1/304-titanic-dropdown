import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


# Global variables
tabtitle = 'Titanic!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/plotly-dash-apps/304-titanic-dropdown'


# Load data for anlysis
# https://github.com/austinlasseter/plotly_dash_tutorial/blob/master/00%20resources/titanic.csv
df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter"
                 "/plotly_dash_tutorial/master/00%20resources/titanic.csv")
df['Female'] = df['Sex'].map({'male': 0, 'female': 1})
df['Cabin Class'] = df['Pclass'].map({1: 'first', 2: 'second', 3: 'third'})
variables_list = ['Survived', 'Female', 'Fare', 'Age']

# app server config
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

# app component layout
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id = 'dropdown',
        options = [{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]),
    html.Br(),
    dcc.Graph(id = 'display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])

# callback
@app.callback(
    Output('display-value', 'figure'),
    [Input('dropdown', 'value')])
def display_value(option):
    grouped_mean = df.groupby(['Cabin Class', 'Embarked'])[option].mean()
    results = pd.DataFrame(grouped_mean)

    # Create a grouped bar chart
    data1 = go.Bar(
        x=results.loc['first'].index,
        y=results.loc['first'][option],
        name='First Class',
        marker=dict(color=color1)
    )
    data2 = go.Bar(
        x=results.loc['second'].index,
        y=results.loc['second'][option],
        name='Second Class',
        marker=dict(color=color2)
    )
    data3 = go.Bar(
        x=results.loc['third'].index,
        y=results.loc['third'][option],
        name='Third Class',
        marker=dict(color=color3)
    )

    layout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Port of Embarkation'), # x-axis label
        yaxis = dict(title = str(option)), # y-axis label

    )
    return go.Figure(data=[data1, data2, data3], layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True)
