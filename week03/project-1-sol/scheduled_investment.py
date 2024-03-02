import pandas as pd
import datetime as dt

RAW_DATA_NAME = "data/QQQ.csv"
ANALYSIS_RESULT_DATA_NAME = "data/QQQ-result.csv"
ANALYSIS_FIXED_RESULT_DATA_NAME = "data/QQQ-result-fixed-cost.csv"
ANALYSIS_FIXED_SELL_RESULT_DATA_NAME = "data/QQQ-result-fixed-cost-sell.csv"


def read_data(file_name=RAW_DATA_NAME) -> pd.DataFrame:
    return pd.read_csv(file_name)


def write_data(data: pd.DataFrame, file_name: str = ANALYSIS_RESULT_DATA_NAME) -> None:
    return data.to_csv(file_name, index=False, float_format='%.4f')


def is_monday(day: str) -> bool:
    return dt.datetime.strptime(day, '%Y-%m-%d').strftime('%A') == 'Monday'


# 从年数，回报倍数得到年化收益. e.g. 0.1 -> 10% 年化收益
def annual_return(num_of_year: int, gain: float, inflation=0) -> float:
    return pow(gain - inflation, 1 / num_of_year) - 1.0


def calculate_scheduled_investment(data: pd.DataFrame, shares: int = 10) -> ():
    positions = [0.0]
    cost = [0.0]
    assets = [0.0]
    percentage = [0.0]
    for i in range(1, len(data)):
        open_price = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        # 实现计算方程，每个周一购买shares，其他日期不购买
        #   如果购买，需要增加position仓位，增加cost花费
        #   如果不购买，append前日仓位和花费
        #   然后总需要根据open_price计算asset, 并且加入assets
        if is_monday(date):
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


def export_result() -> float:
    # 生成 {first_name}_QQQ-result.csv, 目标是跟QQQ-result-expected.csv 一致
    # 在这里调用 calculate_scheduled_investment, 并且赋值
    # 到asset 和cost.
    # 最后返回十年的年化率
    df = read_data()
    df['POSITIONS'], cost, assets, percentage = calculate_scheduled_investment(df)
    df['COST'] = cost
    df['ASSETS'] = assets
    df['PERCENTAGE'] = percentage
    write_data(df, ANALYSIS_RESULT_DATA_NAME)
    return annual_return(10, assets[-1] / cost[-1])  # 10 years


# -- Recommend to copy and write to a new .csv file, so we will not mix Part 3 with Part 1 or 2
def calculate_scheduled_investment_fixed_cost(data: pd.DataFrame, fixed_cost: float = 1000) -> ():
    positions = [0.0]
    cost = [0.0]
    assets = [0.0]
    percentage = [0.0]
    for i in range(1, len(data)):
        open_price = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        # 实现计算方程，每个周一购买shares，其他日期不购买
        #   如果购买，需要增加position仓位，增加cost花费
        #   如果不购买，append前日仓位和花费
        #   然后总需要根据open_price计算asset, 并且加入assets
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


def get_annual_return_fixed_cost() -> float:
    df = read_data()
    df['POSITIONS'], cost, assets, percentage = calculate_scheduled_investment_fixed_cost(df)
    df['COST'] = cost
    df['ASSETS'] = assets
    df['PERCENTAGE'] = percentage
    write_data(df, ANALYSIS_FIXED_RESULT_DATA_NAME)
    return annual_return(10, assets[-1] / cost[-1])  # 10 years


def calculate_scheduled_investment_fixed_cost_with_sell(data: pd.DataFrame,
                                                        fixed_cost: float = 1000,
                                                        sell_multiply: float = 2.0,
                                                        sell_percentage: float = 0.25) -> ():
    """

    :param sell_multiply:
    :param fixed_cost:
    :param data:
    :param sell_percentage: e.g. we can sell 25%.
    :return:
    """
    positions = [0.0]
    cost = [0.0]
    assets = [0.0]
    percentage = [0.0]
    min_asset = 30000
    min_days = 5
    profit = 0
    days = 0
    for i in range(1, len(data)):
        open_price = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        if assets[i - 1] >= min_asset and days >= min_days and assets[i - 1] >= sell_multiply * cost[i - 1]:
            # sell
            sell_share = int(positions[i - 1] * sell_percentage)
            positions.append(positions[i - 1] - sell_share)
            cost.append(cost[i - 1] - cost[i - 1] / positions[i - 1] * sell_share)
            assets.append(assets[i - 1] - assets[i - 1] / positions[i - 1] * sell_share)
            profit += assets[i - 1] - assets[i]
            days = 0
            if cost[i] > 0:
                percentage.append(assets[i] / cost[i])
            else:
                percentage.append(0)
            continue
        else:
            days += 1

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


def get_annual_return_fixed_cost_with_sell() -> float:
    df = read_data()
    df['POSITIONS'], cost, assets, percentage = calculate_scheduled_investment_fixed_cost_with_sell(df)
    df['COST'] = cost
    df['ASSETS'] = assets
    df['PERCENTAGE'] = percentage
    write_data(df, ANALYSIS_FIXED_SELL_RESULT_DATA_NAME)
    return annual_return(10, assets[-1] / cost[-1])  # 10 years


def print_all_annual_returns() -> (float, float, float):
    print("Investment Return 1: ", round(export_result(), 4) * 100, "%")
    print("Investment Return 2: ", round(get_annual_return_fixed_cost(), 4) * 100, "%")
    print("Investment Return 3: ", round(get_annual_return_fixed_cost_with_sell(), 4) * 100, "%")


def print_inflation_adjust_annual_returns() -> (float, float, float):
    print_all_annual_returns()
    total_years = 10
    cum_inflation = (1 + 0.03) ** (total_years - 1) - 1
    print("Cumulative inflation rate: ", cum_inflation)

    invest1 = read_data(ANALYSIS_RESULT_DATA_NAME)
    return1 = annual_return(total_years, invest1['ASSETS'].iloc[-1] / invest1['COST'].iloc[-1], cum_inflation)
    invest2 = read_data(ANALYSIS_FIXED_RESULT_DATA_NAME)
    return2 = annual_return(total_years, invest2['ASSETS'].iloc[-1] / invest2['COST'].iloc[-1], cum_inflation)
    invest3 = read_data(ANALYSIS_FIXED_SELL_RESULT_DATA_NAME)
    return3 = annual_return(total_years, invest3['ASSETS'].iloc[-1] / invest3['COST'].iloc[-1], cum_inflation)

    print("Adjusted Investment Return 1: ", round(return1, 4) * 100, "%")
    print("Adjusted Investment Return 2: ", round(return2, 4) * 100, "%")
    print("Adjusted Investment Return 3: ", round(return3, 4) * 100, "%")


if __name__ == '__main__':
    print_inflation_adjust_annual_returns()
