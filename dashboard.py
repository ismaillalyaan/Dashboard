import dash
from dash import html
from dash import dcc
from dash.dependencies import Input , Output
import pandas as pd
import plotly.express as px
data = pd.read_csv('covid_19_clean_complete.csv')
app = dash.Dash()

app.layout = html.Div([
    html.H1("COVID-19 Dashboard", style={'textAlign': 'center'}),

  
    html.Div([
        html.Label("Select a Country:"),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in data['Country/Region'].unique()],
            value='World'
        )
    ], ),

    html.Div(id='stats', style={'textAlign': 'center'}),
    dcc.Graph(id='line-chart', style={'marginTop': '20px'}),
    dcc.Graph(id='bar-chart', style={'marginTop': '20px'}),
    dcc.Graph(id='map', style={'marginTop': '20px'})
])
@app.callback(
    [Output('stats', 'children'),
     Output('line-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('map', 'figure')],
    [Input('dropdown', 'value')]
)
def update(country):
    if country == 'World':
        filtered = data
    else:
        filtered = data[data['Country/Region'] == country]
    total_confirmed = filtered['Confirmed'].sum()
    total_deaths = filtered['Deaths'].sum()
    total_recovered = filtered['Recovered'].sum()
    stats = [
        html.H4(f"Confirmed: {total_confirmed}"),
        html.H4(f"Deaths: {total_deaths}"),
        html.H4(f"Recovered: {total_recovered}")
    ]
    trend = filtered.groupby('Date')[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()
    line = px.line(trend, x='Date', y=['Confirmed', 'Deaths', 'Recovered'], title='Trends Over Time')
    if country == 'World':
        top_countries = data.groupby('Country/Region')[['Confirmed']].sum().nlargest(5, 'Confirmed').reset_index()
        bar = px.bar(top_countries, x='Country/Region', y='Confirmed', title='Top 5 Countries')
    else:
        bar = px.bar(filtered, x='Date', y='Confirmed', title=f'{country} Daily Cases')
    map = px.scatter_geo(filtered, lat='Lat', lon='Long', size='Confirmed', title='Map of Cases')
    return stats, line, bar, map
if __name__ == '__main__':
    app.run_server(debug=True)