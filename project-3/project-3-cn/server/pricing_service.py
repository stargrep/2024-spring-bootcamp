import pandas as pd
from database_service import execute_read
from database_service import execute_write
from database_service import create_connection
from sqlite3 import Error
from pandas_datareader import data


def update_pricing_data(symbol: str) -> int:
    start = pd.to_datetime('2015-01-01')
    end = pd.to_datetime(today())
    df = data.DataReader(symbol, 'stooq', start, end)

    # TODO [3] implement logic to update `stock_price` table use database_service methods.
    # if the stock symbol already exist, check the most recent `trade_date` and append new records.
    # if the stock symbol doesn't exist, just add all prices.
    # replace the placeholder return with updated record count.
    # return -1 means update failed.

    conn = create_connection()
    try:
        # 检查股票符号是否已经存在于数据库中
        query = f"SELECT COUNT(*) FROM stock_price WHERE symbol = '{symbol}'"
        result = execute_read(query)
        exists_in_database = result[0][0] > 0
        if exists_in_database:
            # 如果股票符号已经存在，获取最近的 trade_date
            query = f"SELECT MAX(trade_date) FROM stock_price WHERE symbol = '{symbol}'"
            result = execute_read(query)
            latest_trade_date = result[0][0] if result[0][0] is not None else '2015-01-01'
            # 筛选出大于最近 trade_date 的数据
            new_records = df[df.index > pd.to_datetime(latest_trade_date)]
            # 如果有新数据，则插入数据库
            if not new_records.empty:
                for index, row in new_records.iterrows():
                    execute_write(f"INSERT INTO stock_price (symbol, trade_date, price) VALUES ('{symbol}', '{index.date()}', {row['Close']})")
                return len(new_records)
            else:
                return 0  # 没有新数据需要更新
        else:
            # 如果股票符号不存在，直接添加所有价格
            for index, row in df.iterrows():
                execute_write(f"INSERT INTO stock_price (symbol, trade_date, price) VALUES ('{symbol}', '{index.date()}', {row['Close']})")
            return len(df)
    except Error as e:
        print(f"An error occurred: {e}")
        return -1
    finally:
        conn.close()

