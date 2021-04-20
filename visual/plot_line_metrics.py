import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

def get_data(connection, metric: str, aggregation: str):
    df = pd.read_sql(f'SELECT * FROM talkpage_metrics WHERE metric_name=="{metric}"', conn)
    df_agg = (
        df.groupby(by=['year_month'])
          .agg({'abs_actual_value': aggregation})
          .rename(columns={'abs_actual_value': f'{aggregation}_value'})
          .reset_index()
    )
    print(df_agg)
    return df_agg


def main():
    conn = sqlite3.connect('../vandal-ca.db')

    fig = go.Figure(
        layout={
            "title": "Toxicity vs Vandalism in Catalan Talk Pages",
            "width": 800,
            "height": 500,
            "xaxis_title": 'Years',
            "yaxis_title": 'Values',
        }
    )

    vandalism_sum = get_data(conn, "toxicity", "sum")
    fig.add_trace(
        go.Scatter(
            x=vandalism_sum["year_month"],
            y=vandalism_sum["sum_value"],
            name='Toxicity',
            line=dict(color='#bc5090', width=2)
        )
    )

    vandalism_sum = get_data(conn, "vandalism", "sum")
    fig.add_trace(
        go.Scatter(
            x=vandalism_sum["year_month"],
            y=vandalism_sum["sum_value"],
            name='Vandalism',
            line=dict(color='#58508d', width=2)
        )
    )

    fig.show()


if __name__ == "__main__":
    main()