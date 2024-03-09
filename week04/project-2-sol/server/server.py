import pandas as pd
from flask import Flask
from flask import request
from calculation_service import write_data_for_symbol, get_annual_return_fixed_cost, annual_return

app = Flask(__name__)


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
    df = pd.read_json("client_rate.json")
    return df.to_dict()


@app.route("/rate/<client_id>")
def get_client_rate(client_id):
    """
    End point for getting rate for a client_id.

    :param client_id: str
    :return: http response
    """
    rates = get_client_rates()
    if client_id in rates:
        return str(rates[client_id]['rate'])
    return '0'


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


@app.route("/calculate_return/<symbol>", methods=['GET'])
def calculate_return(symbol):
    try:
        write_data_for_symbol(symbol)
        asset, cost = get_annual_return_fixed_cost()
        return annual_return(symbol, asset, cost)
    except:
        return "Not able to calculate, likely a wrong symbol name"


if __name__ == "__main__":
    app.run()
