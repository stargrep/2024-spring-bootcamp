import pandas as pd
import datetime as dt

OPEN = 'open_price'
DATE = 'trade_date'


def read_data_from_db(symbol: str, start: str, end: str) -> pd.DataFrame:
    # TODO [4] - Implement read data from stock price db using start date, end date and symbol
    return None


def write_data(symbol: str,
               start: str,
               end: str,
               annual: float,
               asset: float,
               cost: float) -> None:
    # TODO [5] - Implement insert a new result to strategy_return for given symbol.
    # If you have more time, you can add a new field for max_withdraw and sharpe_ratio to catch risk
    return None


def is_monday(day: str) -> bool:
    return dt.datetime.strptime(day, '%Y-%m-%d').strftime('%A') == 'Monday'


def get_annual_return(asset: float, cost: float) -> float:
    times = asset / cost
    num_of_year = 5
    return round((100 * (pow(times, 1 / num_of_year) - 1.0)), 3)


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


def get_annual_return_fixed_cost(symbol: str, start: str, end: str) -> ():
    df = read_data_from_db(symbol, start, end)
    df['POSITIONS'], costs, assets, percentage = calculate_scheduled_investment_fixed_cost(df)
    df['COST'] = costs
    df['ASSETS'] = assets
    df['PERCENTAGE'] = percentage

    asset = assets[-1]
    cost = costs[-1]
    annual_return = get_annual_return(asset, cost)
    write_data(symbol, start, end)
    return asset, cost, annual_return
