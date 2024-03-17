from flask import Flask, jsonify
from flask import request
from flask import json
from calculation_service import write_data_for_symbol, get_annual_return_fixed_cost, annual_return
import pandas as pd
#df = pd.read_json("server/client_rate.json")



#%%
app = Flask(__name__)


# -- DO NOT EDIT
# sample end point for HTTP Get
@app.route("/")
def default():
    """
    default endpoint for this server, just for demo.

    :return: str
    """
    return "PROJECT 3 - we have " + str(len(get_client_rates())) + " clients in total."


# sample data load function
# This is a temporary data file - when we get to know more about database and cloud storage
# we would not be using this kind of data storage.
def get_client_rates():
    """
    return all the client - rate pairs we have.

    :return: dict {id: {'rate':float}}
    """
    import pandas as pd
    df = pd.read_json("client_rate.json")
    return df.to_dict()


# -- DO NOT EDIT END


# -- TODO: Part 1 - add an endpoint to get rate by client id
# When query http://hostname/rate/client1 it would return the rate number for client1 - 0.2
@app.route("/rate/<client_id>")
def get_client_rate(client_id):
    """
    End point for getting rate for a client_id.

    :param client_id: str
    :return: http response
    """
    df = get_client_rates()
    real_rate = df[client_id]
    # How to get the actual rate from client_id?
    return real_rate


# -- TODO END: Part 1


# -- TODO: Part 4 - add an endpoint to add more client and rates data
@app.route("/rate", methods=['POST'])
def upsert_client_rate():
    """
    End point for updating or inserting client rate values in the post param.

    :return: http response.
    """
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    client_id = data.get('client_id')
    rate = data.get('rate')

    if client_id is None or rate is None:
        return jsonify({'error': 'Client ID or Rate is missing'}), 400

    update_client_rates(client_id, rate)  # 更新客户端利率数据

    return jsonify({'message': 'Client rate updated successfully'}), 200


def update_client_rates(client_id, rate):
    """
    update or insert a client_id - rate pair.

    :param client_id: string, e.g. 'client1'
    :param rate: float, e.g. 0.1
    :return:
    """
    # 读取原始数据
    with open("client_rate.json", "r") as file:
        client_rates = json.load(file)

    # 更新或插入数据
    client_rates[client_id] = {'rate': rate}

    # 写入更新后的数据
    with open("client_rate.json", "w") as file:
        json.dump(client_rates, file, indent=4)


# -- TODO END: Part 4

# -- TODO: Part 7 - call calculation_service to display
# If found symbol, like 'QQQ' or 'GOOG', show "USO's Annual Return in the past 5 years is x"
# If not a valid symbol, show "Not able to calculate, likely a wrong symbol name"
@app.route("/calculate_return/<symbol>", methods=['GET'])
def calculate_return(symbol):
    # FIXME - Hint, use try-except and look at the import calculation_service in the file.
    def calculate_return(symbol):
    """
    Calculate annual return for the given symbol in the past 5 years.

    :param symbol: str, the symbol of the stock or asset
    :return: str, message indicating the annual return
    """
    try:
        # 调用计算服务来计算给定符号的年回报率
        annual_return = calculate_annual_return(symbol)

        # 返回计算结果消息
        return f"{symbol}'s Annual Return in the past 5 years is {annual_return}"
    except Exception as e:
        # 如果发生异常（比如找不到符号），返回错误消息
        return "Not able to calculate, likely a wrong symbol name"
    pass


# -- TODO END: Part 7


if __name__ == "__main__":
    app.run()
