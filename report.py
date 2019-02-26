#!/usr/bin/env python

import pymysql.cursors
import pandas as pd
from datetime import datetime
from datetime import timedelta

import graph
from password.password import *

conn = pymysql.connect(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASSWORD,
    db=DATABASE,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def get_daily_report(site_id):
    res = 'Daily report\n\n'
    g = []

    dt = datetime.now()
    with conn.cursor() as cursor:
        for i in range(0, 24):
            try:
                t1 = dt.strftime("%Y-%m-%d {0:02d}:00:00".format(i))
                t2 = dt.strftime("%Y-%m-%d {0:02d}:59:59".format(i))
                sql = "SELECT wattage FROM sensors WHERE id = %s AND created_at BETWEEN %s AND %s"
                cursor.execute(sql, (site_id, t1, t2))
                l = cursor.fetchall()
                df = pd.io.json.json_normalize(l)
                s = round(df.sum()[0]/60, 2)

                g.append((t1, df.sum()[0]/60))
                res += t1 + '\t' + str(s) + '[kWh]\n'
            except IndexError:
                break
    graph.create_graph_image(g)
    return res

def low_power_alert(site_id):
    dt = datetime.now() - timedelta(hours=1)
    with conn.cursor() as cursor:
        try:
            t1 = dt.strftime("%Y-%m-%d %H:00:00")
            t2 = dt.strftime("%Y-%m-%d %H:59:59")
            sql = "SELECT wattage FROM sensors WHERE id = %s AND created_at BETWEEN %s AND %s"
            cursor.execute(sql, (site_id, t1, t2))
            l = cursor.fetchall()
            df = pd.io.json.json_normalize(l)
            if (df.sum()[0]/60) < 2:
                return True, df.sum()[0]/60
        except IndexError:
            break
    return False


def get_site_info():
    with conn.cursor() as cursor:
        sql = "SELECT id, name FROM sites"
        cursor.execute(sql)
        res = cursor.fetchall()
    return res

if __name__ == '__main__':
    print(get_daily_report(10))