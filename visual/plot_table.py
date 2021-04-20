import pandas as pd
import dash
import dash_table
import dash_html_components as html
import sqlite3

conn = sqlite3.connect('../full-it.db')
cursor =conn.cursor()
# cursor.execute('SELECT * FROM talkpage_metrics WHERE metric_name=="toxicity"')

df = pd.read_sql('SELECT * FROM talkpage_metrics WHERE metric_name=="toxicity"', conn)

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("Toxicity activity", style={'text-align': 'center'}),

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode="multi",
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)