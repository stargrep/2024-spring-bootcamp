import pandas as pd
import datetime as dt

RAW_DATA_NAME = "data/QQQ.csv"
ANALYSIS_RESULT_DATA_NAME = "data/QQQ-result.csv"
ANALYSIS_FIXED_RESULT_DATA_NAME = "data/QQQ-result-fixed-cost.csv"
ANALYSIS_FIXED_SELL_RESULT_DATA_NAME = "data/QQQ-result-fixed-cost-sell.csv"

""" DO NOT EDIT (BEGIN) """


def read_data(file_name=RAW_DATA_NAME) -> pd.DataFrame:
    return pd.read_csv(file_name)


def write_data(data: pd.DataFrame, file_name: str = ANALYSIS_RESULT_DATA_NAME) -> None:
    return data.to_csv(file_name, index=False, float_format='%.4f')


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
    for i in range(1, len(data)):
        open_price = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        # 实现计算方程，每个周一购买shares，其他日期不购买
        #   如果购买，需要增加position仓位，增加cost花费
        #   如果不购买，append前日仓位和花费
        #   然后总需要根据open_price计算asset, 并且加入assets
        if is_monday(date):
            positions.append(positions[-1] + 10)
        else:
            positions.append(positions[-1])
        assets.append(open_price * positions[-1])
    print(len(positions))
    return positions, cost, assets


# -- TODO: Part 1 (END)


# -- TODO: Part 2 (START)
def export_result() -> float:
    # 生成 {first_name}_QQQ-result.csv, 目标是跟QQQ-result-expected.csv 一致
    # 在这里调用 calculate_scheduled_investment, 并且赋值
    # 到asset 和cost.
    # 最后返回十年的年化率
    asset = [1]  # replace
    cost = [1]  # replace
    return annual_return(10, asset[-1] / cost[-1])  # 10 years


# -- TODO: Part 2 (END)

# -- TODO: Part 3 (START)
# -- Recommend to copy and write to a new .csv file, so we will not mix Part 3 with Part 1 or 2
def calculate_scheduled_investment_fixed_cost(data: pd.DataFrame) -> ():
    pass


def get_annual_return_fixed_cost() -> float:
    pass


# -- TODO: Part 3 (END)


# -- TODO: Part 4 (START)
def calculate_scheduled_investment_fixed_cost_with_sell(data: pd.DataFrame,
                                                        sell_point: float,
                                                        sell_percentage: float) -> ():
    """

    :param data:
    :param sell_point: e.g. when asset equals to double of cost we can sell.
    :param sell_percentage: e.g. we can sell 25%.
    :return:
    """
    pass


def get_annual_return_fixed_cost_with_sell() -> float:
    pass


# -- TODO: Part 4 (END)


# -- TODO: Part 5 (Bonus)
def print_all_annual_returns() -> (float, float, float):
    # implement - this can simply call the three investment calculation, where they will write three files.
    print("Investment Return 1: ", round(export_result(), 4) * 100, "%")
    print("Investment Return 2: ", round(get_annual_return_fixed_cost(), 4) * 100, "%")
    print("Investment Return 3: ", round(get_annual_return_fixed_cost_with_sell(), 4) * 100, "%")


def print_inflation_adjust_annual_returns() -> (float, float, float):
    print_all_annual_returns()
    # implement - this can simply read from the three files generated.
    return1 = 0
    return2 = 0
    return3 = 0
    print("Adjusted Investment Return 1: ", round(return1, 4) * 100, "%")
    print("Adjusted Investment Return 2: ", round(return2, 4) * 100, "%")
    print("Adjusted Investment Return 3: ", round(return3, 4) * 100, "%")


# -- TODO: Part 5 (END)


if __name__ == '__main__':
    print(calculate_scheduled_investment(read_data()))
    print("Investment Return: ", export_result())
