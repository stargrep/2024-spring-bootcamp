import pandas as pd

from dateutil.utils import today
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
    return -1
