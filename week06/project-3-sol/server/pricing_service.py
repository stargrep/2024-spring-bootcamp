import pandas as pd

from dateutil.utils import today
from pandas_datareader import data
from database_service import *
from datetime import datetime


def update_pricing_data(symbol: str) -> int:
    start = pd.to_datetime('2015-01-01')
    end = pd.to_datetime(today())
    df = data.DataReader(symbol, 'stooq', start, end)
    df['Trade_date'] = df.index

    try:
        res = execute_read(f"SELECT symbol FROM stock_price WHERE symbol = '{symbol}'")
        if res is None or len(res) == 0:
            for i, row in df.iterrows():
                trade_date = row['Trade_date']
                open_price = row['Open']
                high_price = row['High']
                low_price = row['Low']
                close_price = row['Close']
                volume = row['Volume']
                # insert
                execute_write(f"INSERT INTO stock_price VALUES('{symbol}', '{trade_date}', {open_price}"
                              f",{high_price},{low_price},{close_price},{volume})")
            return df.shape[0]
        else:
            latest_time = execute_read(f"SELECT trade_date FROM stock_price WHERE symbol = '{symbol}' "
                                      f"ORDER BY trade_date DESC LIMIT 1")
            latest_date_time = datetime.strptime(latest_time[0][0], '%Y-%m-%d %H:%M:%S')
            count = 0
            for i, row in df.iterrows():
                trade_date = row['Trade_date']
                trade_date_time = datetime.fromtimestamp(trade_date.timestamp())
                open_price = row['Open']
                high_price = row['High']
                low_price = row['Low']
                close_price = row['Close']
                volume = row['Volume']
                if trade_date_time > latest_date_time:
                    # insert
                    execute_write(f"INSERT INTO stock_price VALUES('{symbol}', '{trade_date}', {open_price}"
                                  f",{high_price},{low_price},{close_price},{volume})")
                    count += 1
            return count
    except Exception as e:
        print(e)
        return -1
