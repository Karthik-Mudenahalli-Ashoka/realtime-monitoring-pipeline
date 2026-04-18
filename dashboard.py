import sqlite3
import pandas as pd
import threading
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from src.generator import stream_data
from src.anomaly_detector import detect_anomalies

# Start data generator in background thread
def start_streaming():
    stream_data(duration_seconds=300)  # Stream for 5 minutes

thread = threading.Thread(target=start_streaming, daemon=True)
thread.start()

# Build Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("🖥️ Real-Time Server Monitoring Dashboard",
            style={'textAlign': 'center', 'color': '#2c3e50'}),

    html.Div([
        html.Div(id='total-records', style={'textAlign': 'center',
                 'fontSize': '20px', 'padding': '10px'}),
        html.Div(id='anomaly-count', style={'textAlign': 'center',
                 'fontSize': '20px', 'color': 'red', 'padding': '10px'}),
    ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '50px'}),

    dcc.Graph(id='cpu-graph'),
    dcc.Graph(id='memory-graph'),
    dcc.Graph(id='network-graph'),

    dcc.Interval(id='interval', interval=2000, n_intervals=0)  # refresh every 2s
])

def load_data():
    conn = sqlite3.connect('pipeline.db')
    df = pd.read_sql_query(
        "SELECT * FROM metrics ORDER BY id DESC LIMIT 100", conn
    )
    conn.close()
    # Run anomaly detection on latest data
    detect_anomalies()
    conn = sqlite3.connect('pipeline.db')
    df = pd.read_sql_query(
        "SELECT * FROM metrics ORDER BY id DESC LIMIT 100", conn
    )
    conn.close()
    return df.sort_values('id')

@app.callback(
    [Output('cpu-graph', 'figure'),
     Output('memory-graph', 'figure'),
     Output('network-graph', 'figure'),
     Output('total-records', 'children'),
     Output('anomaly-count', 'children')],
    Input('interval', 'n_intervals')
)
def update_graphs(n):
    df = load_data()

    anomalies = df[df['is_anomaly'] == 1]
    normal = df[df['is_anomaly'] == 0]

    def make_graph(col, title, color, unit):
        return {
            'data': [
                go.Scatter(x=normal['timestamp'], y=normal[col],
                          mode='lines', name='Normal',
                          line=dict(color=color)),
                go.Scatter(x=anomalies['timestamp'], y=anomalies[col],
                          mode='markers', name='Anomaly',
                          marker=dict(color='red', size=12, symbol='x'))
            ],
            'layout': go.Layout(
                title=title,
                xaxis={'title': 'Time'},
                yaxis={'title': unit},
                plot_bgcolor='#f8f9fa',
                hovermode='x unified'
            )
        }

    cpu_fig = make_graph('cpu_usage', 'CPU Usage', '#3498db', '% Usage')
    mem_fig = make_graph('memory_usage', 'Memory Usage', '#2ecc71', '% Usage')
    net_fig = make_graph('network_io', 'Network I/O', '#9b59b6', 'MB/s')

    total = f"📊 Total Records: {len(df)}"
    anomaly_text = f"🚨 Anomalies Detected: {len(anomalies)}"

    return cpu_fig, mem_fig, net_fig, total, anomaly_text

if __name__ == '__main__':
    app.run(debug=False, port=8050)