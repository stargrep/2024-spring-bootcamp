import pandas as pd
import datetime as dt
from pandas_datareader import data

RAW_DATA_NAME = "data/data.csv"
ANALYSIS_FIXED_RESULT_DATA_NAME = "data/calculated.csv"
OPEN = 'Open'
DATE = 'Date'


def read_data() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_NAME)


def write_data(data: pd.DataFrame, file_name: str = RAW_DATA_NAME) -> None:
    return data.to_csv(file_name, index=False)


def is_monday(day: str) -> bool:
    return dt.datetime.strptime(day, '%Y-%m-%d').strftime('%A') == 'Monday'


def annual_return(symbol: str, asset: float, cost: float) -> str:
    times = asset / cost
    num_of_year = 5
    return symbol + "'s Annual Return in the past 5 years is {:.3f}%".format(100 * (pow(times, 1 / num_of_year) - 1.0))


def calculate_scheduled_investment_fixed_cost(data: pd.DataFrame, fixed_cost: float = 1000) -> ():
    positions = [0.0]
    cost = [0.0]
    assets = [0.0]
    percentage = [0.0]
    for i in range(1, len(data)):
        open_price = data.iloc[i][OPEN]
        date = data.iloc[i][DATE]
        if is_monday(date):
            shares = fixed_cost // open_price
            positions.append(positions[-1] + shares)
            cost.append(cost[i - 1] + open_price * shares)
        else:
            positions.append(positions[-1])
            cost.append(cost[i - 1])
        assets.append(open_price * positions[-1])
        if cost[i] > 0:
            percentage.append(assets[i] / cost[i])
        else:
            percentage.append(0)
    return positions, cost, assets, percentage


def get_annual_return_fixed_cost() -> ():
    df = read_data()
    df['POSITIONS'], cost, assets, percentage = calculate_scheduled_investment_fixed_cost(df)
    df['COST'] = cost
    df['ASSETS'] = assets
    df['PERCENTAGE'] = percentage
    write_data(df, ANALYSIS_FIXED_RESULT_DATA_NAME)
    return assets[-1], cost[-1]


def write_data_for_symbol(symbol: str) -> None:
    start = pd.to_datetime('2015-01-01')
    end = pd.to_datetime('2022-01-01')
    # google stock API
    df = data.DataReader(symbol, 'stooq', start, end)
    df[DATE] = df.index
    write_data(df.loc[::-1], RAW_DATA_NAME)
