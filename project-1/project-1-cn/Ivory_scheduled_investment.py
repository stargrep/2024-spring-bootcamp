import pandas as pd
import datetime as dt

RAW_DATA_NAME = "data/QQQ.csv"
ANALYSIS_RESULT_DATA_Ivory = "data/QQQ-result.csv"
ANALYSIS_FIXED_RESULT_DATA_Ivory = "data/QQQ-result-fixed-cost.csv"
ANALYSIS_FIXED_SELL_RESULT_DATA_Ivory = "data/QQQ-result-fixed-cost-sell.csv"

""" DO NOT EDIT (BEGIN) """


# 读取数据
def read_data(file_name=RAW_DATA_NAME) -> pd.DataFrame:
    return pd.read_csv(file_name)


# 输出数据
def write_data(data: pd.DataFrame, file_name: str = ANALYSIS_RESULT_DATA_Ivory) -> None:
    return data.to_csv(file_name, index=False, float_format='%.4f')


# 判断是否为星期一
def is_monday(day: str) -> bool:
    return dt.datetime.strptime(day, '%Y-%m-%d').strftime('%A') == 'Monday'


# 从年数，回报倍数得到年化收益. e.g. 0.1 -> 10% 年化收益
def annual_return(num_of_year: int, gain: float, inflation=0) -> float:
    return pow(gain - inflation, 1 / num_of_year) - 1.0


""" DO NOT EDIT (END) """


# -- TODO: Part 1 (START)
def calculate_scheduled_investment(data: pd.DataFrame) -> ():
    shares = 10
    positions = [0.0]
    cost = [0.0]
    assets = [0.0]
    percentage = [0.0]
    for i in range(1, len(data)):
        open_price = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        #   实现计算方程，每个周一购买shares，其他日期不购买
        #   如果购买，需要增加position仓位，增加cost花费
        #   如果不购买，append前日仓位和花费
        #   然后总需要根据open_price计算asset, 并且加入assets
        if is_monday(date):
            current_cost = shares * open_price
            positions.append(positions[-1] + shares)
            cost.append(cost[i-1] + current_cost)
        else:
            positions.append(positions[-1])
            cost.append(cost[i-1])
        current_asset = open_price * positions[-1]
        assets.append(current_asset)
        if cost[i] > 0:
            percentage.append(assets[i] / cost[i])
        else:
            percentage.append(0)
    print(len(positions))
    return positions, cost, assets, percentage


# -- TODO: Part 1 (END)


# -- TODO: Part 2 (START)
def get_annual_return() -> float:
    # 生成 {first_name}_QQQ-result.csv, 目标是跟QQQ-result-expected.csv一致
    # 在这里调用 calculate_scheduled_investment, 并且赋值到asset和cost
    # 最后返回十年的年化率
    data = read_data()
    positions, cost, assets, percentage = calculate_scheduled_investment(data)
    data["POSITIONS"] = positions
    data["COST"] = cost
    data["ASSETS"] = assets
    data["PERCENTAGE"] = percentage
    write_data(data, ANALYSIS_RESULT_DATA_Ivory)
    return annual_return(10, assets[-1] / cost[-1])  # 10 years


# -- TODO: Part 2 (END)

# -- TODO: Part 3 (START)
# -- Recommend to copy and write to a new .csv file, so we will not mix Part 3 with Part 1 or 2
def calculate_scheduled_investment_fixed_cost(data: pd.DataFrame, fixed_spend: float = 1000.0) -> ():
    fixed_positions = [0.0]
    fixed_cost = [0.0]
    fixed_assets = [0.0]
    fixed_percentage = [0.0]
    for i in range(1, len(data)):
        fixed_open_price = data.iloc[i]['OPEN']
        fixed_date = data.iloc[i]['DATES']
        if is_monday(fixed_date):
            fixed_shares = fixed_spend // fixed_open_price
            fixed_current_cost = fixed_shares * fixed_open_price
            fixed_positions.append(fixed_positions[-1] + fixed_shares)
            fixed_cost.append(fixed_cost[i - 1] + fixed_current_cost)
        else:
            fixed_positions.append(fixed_positions[-1])
            fixed_cost.append(fixed_cost[i - 1])
        fixed_current_asset = fixed_open_price * fixed_positions[-1]
        fixed_assets.append(fixed_current_asset)
        if fixed_cost[i] > 0:
            fixed_percentage.append(fixed_assets[i] / fixed_cost[i])
        else:
            fixed_percentage.append(0)
    print(len(fixed_positions))
    return fixed_positions, fixed_cost, fixed_assets, fixed_percentage


def get_annual_return_fixed_cost() -> float:
    data = read_data()
    fixed_positions, fixed_cost, fixed_assets, fixed_percentage = calculate_scheduled_investment_fixed_cost(data)
    data["POSITIONS"] = fixed_positions
    data["COST"] = fixed_cost
    data["ASSETS"] = fixed_assets
    data["PERCENTAGE"] = fixed_percentage
    write_data(data, ANALYSIS_FIXED_RESULT_DATA_Ivory)
    return annual_return(10, fixed_assets[-1] / fixed_cost[-1])  # 10 years


# -- TODO: Part 3 (END)


# -- TODO: Part 4 (START)
def calculate_scheduled_investment_fixed_cost_with_sell(data: pd.DataFrame,
                                                        fixed_spend: float = 1000.0,
                                                        sell_multiply: float = 2.0,
                                                        sell_percentage: float = 0.25) -> ():
    """
    :param data:
    :param sell_point: e.g. when asset equals to double of cost we can sell.
    :param sell_percentage: e.g. we can sell 25%.
    :return:
    """
    positions_sell = [0.0]
    cost_sell = [0.0]
    assets_sell = [0.0]
    percentage_sell = [0.0]
    min_asset = 30000  # 当资产在30000元以上是考虑卖出
    min_days = 5  # 当剩余交易天数大于五个工作日，即还有下一个星期一
    profit = 0
    days = 0
    for i in range(1, len(data)):
        open_price_sell = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        # sell logic
        if assets_sell[i - 1] >= min_asset and days >= min_days and \
                assets_sell[i - 1] >= sell_multiply * cost_sell[i - 1]:
            sell_share = int(positions_sell[i - 1] * sell_percentage)
            positions_sell.append(positions_sell[i - 1] - sell_share)
            current_cost_sell = cost_sell[i - 1] * (positions_sell[i - 1] - sell_share) / positions_sell[i - 1]
            cost_sell.append(current_cost_sell)
            current_assets_sell = assets_sell[i - 1] * (positions_sell[i - 1] - sell_share) / positions_sell[i - 1]
            assets_sell.append(assets_sell[i-1] - assets_sell[i-1])
            profit += assets_sell[i - 1] - assets_sell[i]
            days = 0
            if cost_sell[i] > 0:
                percentage_sell.append(assets_sell[i] / cost_sell[i])
            else:
                percentage_sell.append(0)
            continue
        else:
            days += 1

        # buy logic
        if is_monday(date):
            shares_sell = fixed_spend // open_price_sell
            positions_sell.append(positions_sell[-1] + shares_sell)
            current_cost_sell = open_price_sell * shares_sell
            cost_sell.append(cost_sell[i - 1] + current_cost_sell)
        else:
            positions_sell.append(positions_sell[-1])
            cost_sell.append(cost_sell[i - 1])
        current_assets = open_price_sell * positions_sell[-1]
        assets_sell.append(current_assets)
        if cost_sell[-1] > 0:
            percentage_sell.append(assets_sell[i] / cost_sell[i])
        else:
            percentage_sell.append(0)
    print(len(positions_sell))
    return positions_sell, cost_sell, assets_sell, percentage_sell


def get_annual_return_fixed_cost_with_sell() -> float:
    data = read_data()
    positions_sell, cost_sell, assets_sell, percentage_sell = calculate_scheduled_investment_fixed_cost_with_sell(data)
    data["POSITIONS"] = positions_sell
    data["COST"] = cost_sell
    data["ASSETS"] = assets_sell
    data["PERCENTAGE"] = percentage_sell
    write_data(data, ANALYSIS_FIXED_SELL_RESULT_DATA_Ivory)
    return annual_return(10, assets_sell[-1] / cost_sell[-1])  # 10 years


# -- TODO: Part 4 (END)


# -- TODO: Part 5 (Bonus)
def print_all_annual_returns() -> (float, float, float):
    # implement - this can simply call the three investment calculation, where they will write three files.
    print("Investment Return 1: ", round(get_annual_return(), 4) * 100, "%")
    print("Investment Return 2: ", round(get_annual_return_fixed_cost(), 4) * 100, "%")
    print("Investment Return 3: ", round(get_annual_return_fixed_cost_with_sell(), 4) * 100, "%")


def print_inflation_adjust_annual_returns() -> (float, float, float):
    print_all_annual_returns()
    total_years = 10
    cum_inflation = (1 + 0.03) ** (total_years - 1) - 1
    print("Cumulative inflation rate: ", cum_inflation)
    invest1 = read_data(ANALYSIS_RESULT_DATA_Ivory)
    return1 = annual_return(total_years, invest1['ASSETS'].iloc[-1] / invest1['COST'].iloc[-1], cum_inflation)
    invest2 = read_data(ANALYSIS_FIXED_RESULT_DATA_Ivory)
    return2 = annual_return(total_years, invest2['ASSETS'].iloc[-1] / invest2['COST'].iloc[-1], cum_inflation)
    invest3 = read_data(ANALYSIS_FIXED_SELL_RESULT_DATA_Ivory)
    return3 = annual_return(total_years, invest3['ASSETS'].iloc[-1] / invest3['COST'].iloc[-1], cum_inflation)
    print("Adjusted Investment Return 1: ", round(return1, 4) * 100, "%")
    print("Adjusted Investment Return 2: ", round(return2, 4) * 100, "%")
    print("Adjusted Investment Return 3: ", round(return3, 4) * 100, "%")


# -- TODO: Part 5 (END)


if __name__ == '__main__':
    print_inflation_adjust_annual_returns()

"""
2516
Investment Return 1:  10.26 %
Investment Return 2:  13.11 %
Investment Return 3:  7.35 %
Cumulative inflation rate:  0.3047731838292449
Adjusted Investment Return 1:  8.92 %
Adjusted Investment Return 2:  12.07 %
Adjusted Investment Return 3:  5.62 %
"""