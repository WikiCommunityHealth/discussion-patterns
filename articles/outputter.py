from talkpage_metrics import MetricDB
import sqlite3

def send_page_data(data):
    conn = sqlite3.connect('test.db', uri=True)

    table_name = 'talkpage_metrics'
    query = ("CREATE TABLE IF NOT EXISTS " + table_name +
             " (page_id integer, page_title text, abs_value real, rel_value real, metric_name text, year_month text, PRIMARY KEY (page_id, metric_name, year_month))")
    conn.execute(query)
    # conn.commit()

    conn.executemany(
        "INSERT INTO " + table_name + " values (?, ?, ?, ?, ?, ?)",
        map(MetricDB.unpack, data)
    )

    conn.commit()
    conn.close()


def send_user_data(data):
    conn = sqlite3.connect('test.db', uri=True)

    table_name = 'user_metrics'
    query = ("CREATE TABLE IF NOT EXISTS " + table_name +
             " (user_id integer, username text, abs_value real, rel_value real, metric_name text, year_month text, PRIMARY KEY (page_id, metric_name, year_month))")
    conn.execute(query)
    # conn.commit()

    conn.executemany(
        "INSERT INTO " + table_name + " values (?, ?, ?, ?, ?, ?)",
        map(MetricDB.unpack, data)
    )

    conn.commit()
    conn.close()
