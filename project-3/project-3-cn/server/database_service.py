import pandas as pd
import sqlite3
from sqlite3 import Error
from os.path import exists


# 用于执行 SQL 查询并将结果以 DataFrame 的形式返回
def execute_read_df(statement):
    conn = create_connection()  # 创建到 SQLite 数据库的连接
    df = pd.read_sql_query(statement, conn)  # 执行 SQL 查询并读取结果
    conn.close()  # 关闭了数据库
    return df


# 用于执行 SQL 查询并返回结果
def execute_read(statement):
    conn = create_connection()
    cursor = conn.cursor()  # 获取数据库游标（对数据库执行操作的控制器）
    try:
        cursor.execute(statement)  # 执行 SQL 查询
        result = cursor.fetchall()  # 获取所有查询结果
        conn.close()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# 执行 SQL 写入操作
def execute_write(statement):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(statement)  # 执行 SQL 写入操作
        conn.commit()  # 提交事务
        print("Write query executed successfully")
    except Error as e:
        print(f"Write error '{e}' occurred")
    conn.close()


# 用于创建到 SQLite 数据库的连接
def create_connection(path="test.db"):  # path指定数据库文件的路径
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# Initialization, load some existing data in data.sql
# 用于从一个名为 "data.sql" 的 SQL 文件中加载数据到数据库中
def load_data(database):
    if exists(database):
        print(f"No need to reload data since {database} exists, delete the file if you want to force reload data.")
        return

    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    sql_file = open("data.sql")  # 打开 "data.sql" 文件，将其内容作为字符串读取
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string) # 执行 SQL 脚本来加载数据
