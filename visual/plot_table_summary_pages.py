from typing import List, Sequence
import pandas as pd
import sqlite3
import time
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


def get_columns():
    return {
        "page_id": -1,
        "num_action_addition": 0.0,
        "num_action_creation": 0.0,
        "num_action_deletion": 0.0,
        "num_action_modification": 0.0,
        "num_action_restoration": 0.0,
        "total_action": 0.0,
        "user_involved": 0.0,
        "max_depth": 0.0,
        "toxicity": 0.0,
        "vandalism": 0.0
    }

def get_metric_table(year_month: str) -> pd.DataFrame:
    now = time.perf_counter()

    conn = sqlite3.connect('../vandal-ca.db')
    # conn = sqlite3.connect('./pages-en-full.db')
    cursor = conn.cursor()
    df = pd.read_sql(f'SELECT * FROM talkpage_metrics WHERE year_month=="{year_month}"', conn)
    grouped = df.groupby("page_id")

    print(f"Number of pages to process: {len(grouped)}")

    pages: List[Sequence[float]] = []

    for name, group in grouped:
        # print(f"Working on page_id {name}")

        page_metrics = get_columns()
        page_metrics["page_id"] = name

        for index, row in group.iterrows():
            page_metrics[row["metric_name"]] = row["abs_actual_value"]

        pages.append(list(page_metrics.values()))

    metrics = pd.DataFrame(
        pages,
        columns=list(get_columns().keys())
    )

    print(f"Elapsed time: {time.perf_counter() - now}")

    return metrics

year_month = "2003-04"
metrics = get_metric_table(year_month)

app = dash.Dash(__name__)
app.layout = html.Div([
    # html.H1(f"Metrics for Catalan Talk Pages during {year_month}", style={'text-align': 'center'}, id="title"),
    html.Div(
        id='title'
    ),


    dcc.Input(
        id="year_month",
        type="text",
        placeholder="YYYY-MM",
    ),

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i, "hideable":True} for i in metrics.columns],
        data=metrics.to_dict('records'),
        sort_action="native",
        sort_mode="multi",
    )
])

@app.callback(
    Output("table", "data"),
    Input("year_month", "value"),
)
def cb_render(year_month: str):
    return get_metric_table(year_month).to_dict('records')

@app.callback(
    Output('title', 'children'),
    Input("year_month", "value"),
)
def update_ticker_header(year_month: str):
    if year_month:
        return [html.H1(f"Metrics for Catalan Talk Pages during {year_month}", style={'text-align': 'center'})]
    else:
        return [html.H1(f"Insert a date in the textbox", style={'text-align': 'center'})]

if __name__ == '__main__':
    app.run_server(debug=True)
