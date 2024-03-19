from flask import Flask  # 从 Flask 库中导入 Flask 类，用于创建 Web 应用程序
from flask import request  # 从 Flask 库中导入 request 对象，用于处理 HTTP 请求
from flask import json
from calculation_service import write_data_for_symbol, get_annual_return_fixed_cost, annual_return

# 基于 Flask 的 Web 应用程序

app = Flask(__name__)  # 创建一个 Flask 应用程序实例，__name__ 是 Python 中的特殊变量，指示当前模块的名称


# -- DO NOT EDIT
# sample end point for HTTP Get
@app.route("/")
def default():  # 定义一个get API，处理根路径 ("/") 的请求
    """
    default endpoint for this server, just for demo.

    :return: str
    """
    return "PROJECT 2 - we have " + str(len(get_client_rates())) + " clients in total."


# sample data load function
# This is a temporary data file - when we get to know more about database and cloud storage
# we would not be using this kind of data storage.
def get_client_rates():
    """
    return all the client - rate pairs we have.

    :return: dict {id: {'rate':float}}
    """
    import pandas as pd
    df = pd.read_json("client_rate.json")  # read_json 函数从名为 "client_rate.json" 的文件中读取数据
    return df.to_dict()  # 将 DataFrame 转换为字典并返回


# -- DO NOT EDIT END


# -- TODO: Part 1 - add an endpoint to get rate by client id
# When query http://hostname/rate/client1 it would return the rate number for client1 - 0.2
@app.route("/rate/<client_id>")  # 新增了一个路由 /rate/<client_id>
def get_client_rate(client_id):  # 接受客户 ID 作为参数，获取客户费率
    """
    End point for getting rate for a client_id.

    :param client_id: str
    :return: http response
    """
    # How to get the actual rate from client_id?
    client_rates = get_client_rates()  # 得到所有客户的费率，返回一个字典
    if client_id in client_rates:  # 检查客户id是否在字典中
        rate = client_rates[client_id]['rate']
        print(f"The rate for {client_id} is {rate}.")
    else:
        print(f"No rate found for {client_id}.")
    return rate


# -- TODO END: Part 1


# -- TODO: Part 4 - add an endpoint to add more client and rates data
@app.route("/rate", methods=['POST'])
def upsert_client_rate():
    """
    End point for updating or inserting client rate values in the post param.

    :return: http response.
    """
    # We want to update if the client exist in the client_rate.json data
    # Or insert a new client-rate pair into client_rate.json data
    client_infor = request.get_json()
    client_rates = get_client_rates()
    if client_infor in client_rates:
        return "No adjustment"
    else:
        client_rates.append({})
        client_rates[-1] = client_infor['rate']
        print("Upsert has done")
        return client_rates


def update_client_rates(client_id, rate):
    """
    update or insert a client_id - rate pair.

    :param client_id: string, e.g. 'client1'
    :param rate: float, e.g. 0.1
    :return:
    """
    # check if exist
    # replace or add client rate
    # re-write the file
    client_infor = request.get_json()
    client_id = client_infor['client_id']
    client_rates = get_client_rates()
    if client_id in client_rates:
        client_rates[client_id] = rate
        print("Update has done")
        return client_rates
    else:
        return "No adjustment"



# -- TODO END: Part 4

# -- TODO: Part 7 - call calculation_service to display
# If found symbol, like 'QQQ' or 'GOOG', show "USO's Annual Return in the past 5 years is x"
# If not a valid symbol, show "Not able to calculate, likely a wrong symbol name"
@app.route("/calculate_return/<symbol>", methods=['GET'])
def calculate_return(symbol):
    # FIXME - Hint, use try-except and look at the import calculation_service in the file.
    write_data_for_symbol(symbol)
    data = get_annual_return_fixed_cost()
    cost = data['COST']
    asset = data['ASSET']
    return annual_return()


# -- TODO END: Part 7


if __name__ == "__main__":
    app.run()
