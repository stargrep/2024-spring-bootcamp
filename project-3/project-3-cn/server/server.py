from flask import Flask
from flask import request
from database_service import execute_read
from database_service import execute_write
from database_service import load_data
from pricing_service import update_pricing_data
from strategy_service import get_annual_return_fixed_cost

app = Flask(__name__)


# -- DO NOT EDIT
@app.route("/")
def default():
    """
    default endpoint for this server, just for demo.

    :return: str
    """
    clients = get_client_rates()
    return "PROJECT 3 - we have " + str(len(clients)) + " clients in total: " + str(clients)


def get_client_rates():
    """
    return all the client - rate pairs we have.

    :return: DataFrame {id, client_id, rate}
    """
    return execute_read("SELECT * from client_rates")


# -- DO NOT EDIT END


# When query http://hostname/rate/client1 it would return the rate number for client1 - 0.2
@app.route("/rate/<client_id>")
def get_client_rate(client_id):
    """
    End point for getting rate for a client_id.

    :param client_id: str
    :return: http response
    """
    # TODO: [1] Implement - get a single client rate and return it, if there is no rate data, then return "0.0".
    query = f"SELECT rate FROM client_rates WHERE client_id = '{client_id}'"
    client_rate = execute_read(query)
    return client_rate


@app.route("/rate", methods=['POST'])
def upsert_client_rate():
    """
    End point for updating or inserting client rate values in the post param.

    :return: http response.
    """
    data = request.get_json()
    update_client_rates(data["client_id"], data["rate"])
    return "SUCCESSFULLY UPDATED!"


def update_client_rates(client_id, rate):
    """
    update or insert a client_id - rate pair.

    :param client_id: string, e.g. 'client1'
    :param rate: float, e.g. 0.1
    :return: None
    """
    # TODO: [2] Implement Insert or Update function for a given client_id and rate. If exists, update, else, insert.
    query = f"SELECT rate FROM client_rates WHERE client_id = '{client_id}'"
    out = execute_read(query)
    if len(out) > 0:
        updated = f"UPDATE client_rates SET rate = {rate} WHERE client_id = '{client_id}"
        execute_write(updated)
        return "SUCCESSFULLY UNDATED!"
    else:
        inserted = f"INSERT INTO client_rates (client_id, rate) VALUES ('{client_id},'{rate}')"
        execute_write(inserted)
        return "SUCCESSFULLY INSERTED"


@app.route("/pricing_etl/<symbol>", methods=['GET'])
def trigger_pricing_etl(symbol):
    update_records = update_pricing_data(symbol)
    if update_records >= 0:
        return f"Updated {update_pricing_data(symbol)} Records for {symbol}."
    else:
        return f"ETL Update failed for {symbol}"


@app.route("/calculate_return/<symbol>", methods=['GET'])
def calculate_return(symbol):
    asset, cost, return_ = get_annual_return_fixed_cost(symbol, '2017-01-01', '2022-01-01')
    return f"5 years annual return for {symbol} is {return_} from 2017 - 2022"


if __name__ == "__main__":
    load_data("test.db")
    app.run(port=5000)
