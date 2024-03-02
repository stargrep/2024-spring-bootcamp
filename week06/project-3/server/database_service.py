import pandas as pd
import sqlite3
from sqlite3 import Error
from os.path import exists


def execute_read_df(statement):
    conn = create_connection()
    df = pd.read_sql_query(statement, conn)
    conn.close()
    return df


def execute_read(statement):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(statement)
        result = cursor.fetchall()
        conn.close()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_write(statement):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(statement)
        conn.commit()
        print("Write query executed successfully")
    except Error as e:
        print(f"Write error '{e}' occurred")
    conn.close()


def create_connection(path="test.db"):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# Initialization, load some existing data in data.sql
def load_data(database):
    if exists(database):
        print(f"No need to reload data since {database} exists, delete the file if you want to force reload data.")
        return

    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    sql_file = open("data.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)
