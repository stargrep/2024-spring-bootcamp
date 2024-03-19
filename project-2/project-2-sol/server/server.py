from flask import Flask  # 从 Flask 库中导入 Flask 类，用于创建 Web 应用程序
from flask import request  # 从 Flask 库中导入 request 对象，用于处理 HTTP 请求
from flask import json
from calculation_service import write_data_for_symbol, get_annual_return_fixed_cost, annual_return
import pandas as pd

# 基于 Flask 的 Web 应用程序

app = Flask(__name__)  # 创建一个 Flask 应用程序实例，__name__ 是 Python 中的特殊变量，指示当前模块的名称


# 定义一个路由，用于处理根路径 ("/") 的请求
@app.route("/")
def default():
    """
    default endpoint for this server, just for demo.

    :return: str
    """
    return "FIRST PROJECT - we have " + str(len(get_client_rates())) + " clients in total."


def get_client_rates():
    """
    return all the client - rate pairs we have.

    :return: dict {id: {'rate':float}}
    """
    import pandas as pd
    df = pd.read_json("client_rate.json")  # read_json 函数从名为 "client_rate.json" 的文件中读取数据
    return df.to_dict()  # 将 DataFrame 转换为字典并返回给客户端


# 新增了一个路由 /rate/<client_id>，用于获取特定客户的费率信息
@app.route("/rate/<client_id>")
def get_client_rate(client_id):  # 接受客户 ID 作为参数，获取客户费率
    """
    End point for getting rate for a client_id.

    :param client_id: str
    :return: http response
    """
    rates = get_client_rates()
    if client_id in rates:
        return str(rates[client_id]['rate'])
    return '0'


# 新增了一个路由 /rate，用于更新或插入客户的费率信息，指定了请求方法为 POST
@app.route("/rate", methods=['POST'])
def upsert_client_rate():
    """
    End point for updating or inserting client rate values in the post param.

    :return: http response.
    """
    param = request.get_json()
    client_id = param['client_id']
    rate = param['rate']

    rates = get_client_rates()
    rates[client_id] = {'rate': rate}
    df = pd.DataFrame.from_dict(rates)
    df.to_json("client_rate.json")
    return request.get_json()


# 定义了一个路由 /calculate_return/<symbol>，用于计算给定资产符号的年回报率，指定了请求方法为 GET
@app.route("/calculate_return/<symbol>", methods=['GET'])
def calculate_return(symbol):
    try:
        write_data_for_symbol(symbol)
        asset, cost = get_annual_return_fixed_cost()
        return annual_return(symbol, asset, cost)
    except:
        return "Not able to calculate, likely a wrong symbol name"


# 检查脚本是否可以被执行
if __name__ == "__main__":
    app.run()
