import dash
from dash import html, dcc, Output, Input, State, ctx
from dash import dash_table
import subprocess
import os
import json

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H2("Call Recording Processor", style={'textAlign': 'center'}),
    html.Div([
        dcc.Input(id='url-input', type='text', placeholder='Enter Convoso API URL',
                  style={'width': '80%', 'marginRight': '10px'}),
        html.Button('Submit', id='submit-btn', n_clicks=0),
        html.Button('Reset', id='reset-btn', n_clicks=0),
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '20px'}),
    html.Div(id='log-output', style={'whiteSpace': 'pre-wrap', 'padding': '10px', 'backgroundColor': '#f0f0f0'}),
    html.Div(id='summary-button'),
    html.Div(id='table-div')
], style={'width': '80%', 'margin': 'auto'})

# Submit: Run main.py
@app.callback(
    Output('log-output', 'children'),
    Output('summary-button', 'children'),
    Input('submit-btn', 'n_clicks'),
    State('url-input', 'value'),
    prevent_initial_call=True
)
def handle_submit(n_clicks, url):
    if not url:
        return "Please provide a URL.", dash.no_update

    command = [r".venv\Scripts\python.exe", "main.py", url]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    logs = ""
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            logs += output

    if not os.path.exists("metadata.json"):
        return logs + "\nERROR: metadata.json not found.", dash.no_update

    return logs + "\nProcessing finished successfully.", html.Button("Show Summary", id="show-summary-btn", n_clicks=0)

# Show summary + metadata
@app.callback(
    Output('table-div', 'children'),
    Input('show-summary-btn', 'n_clicks'),
    prevent_initial_call=True
)
def display_summary(n_clicks):
    if not os.path.exists("metadata.json"):
        return html.Div("No metadata file found.")

    with open("metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Trim transcript and summary
    for entry in metadata:
        entry["transcript"] = entry["transcript"][:100] + "..." if entry.get("transcript") else ""
        entry["summary"] = entry["summary"][:100] + "..." if entry.get("summary") else ""

    return html.Div([
        html.H3("Summary and Metadata Table", style={"textAlign": "center"}),
        dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in metadata[0]],
            data=metadata,
            page_size=10,
            style_cell={'whiteSpace': 'normal', 'textAlign': 'left'},
            style_table={'overflowX': 'auto'},
        )
    ])

# Reset button
@app.callback(
    Output('url-input', 'value'),
    Output('log-output', 'children'),
    Output('summary-button', 'children'),
    Output('table-div', 'children'),
    Input('reset-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_all(n_clicks):
    return "", "", "", ""

if __name__ == '__main__':
    app.run(debug=True)
