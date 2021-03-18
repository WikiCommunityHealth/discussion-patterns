from typing import Sequence
import sqlite3
from .metric_db import MetricDB


def send_page_data(data: Sequence[MetricDB], database_path: str) -> None:
    conn = sqlite3.connect(database_path, uri=True)

    table_name = "talkpage_metrics"
    query = (
        "CREATE TABLE IF NOT EXISTS "
        + table_name
        + " (page_id integer, metric_name text, year_month text, abs_actual_value real, rel_actual_value real, abs_cumulative_value real, rel_cumulative_value real, PRIMARY KEY (page_id, metric_name, year_month))"
    )
    conn.execute(query)
    # conn.commit()

    try:
        conn.executemany(
            "INSERT INTO " + table_name + " values (?, ?, ?, ?, ?, ?, ?)",
            map(MetricDB.unpack, data),
        )

        conn.commit()
    except Exception:
        for el in data:
            print(el.metric_name, el.year_month, el.abs_actual_value, el.abs_cumulative_value)

    conn.close()


def send_user_data(data: Sequence[MetricDB]) -> None:
    conn = sqlite3.connect("users.db", uri=True)

    table_name = "user_metrics"
    query = (
        "CREATE TABLE IF NOT EXISTS "
        + table_name
        + " (user_id integer, metric_name text, year_month text, abs_actual_value real, rel_actual_value real, abs_cumulative_value real, rel_cumulative_value real, PRIMARY KEY (page_id, metric_name, year_month))"
    )
    conn.execute(query)
    # conn.commit()

    conn.executemany(
        "INSERT INTO " + table_name + " values (?, ?, ?, ?, ?, ?, ?)",
        map(MetricDB.unpack, data),
    )

    conn.commit()
    conn.close()
