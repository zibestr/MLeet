from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)


def update_layout(df: pd.DataFrame, project_name: str):
    app.df = df
    metrics = df.columns.tolist()[2:-1]
    app.layout = html.Div([
        html.H1(project_name),
        html.Div([
            html.H2('Each metric data'),
            dcc.Graph(id='each_metric'),
            html.P('Experiment'),
            dcc.Dropdown(
                id='metric_name',
                options=metrics,
                value=metrics[0]
            )
        ])
    ], className='main')


@app.callback(
    Output('each_metric', 'figure'),
    Input('metric_name', 'value')
)
def update_each_metric(metric_name: str):
    df = app.df
    fig = px.bar(x=df['exp_name'].tolist(), y=df[metric_name].tolist(),
                 labels={
                     'x': 'Experiment name',
                     'y': 'Metric score'
                 })

    return fig
