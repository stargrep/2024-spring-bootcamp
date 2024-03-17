from server import server
from flask import Flask, jsonify










# -- TODO: Part 2, write an API client so we are able to query
def get_rate(client_id):
    """
    would expect to return a float rate.

    :param client_id: string, e.g. 'client1'
    :return: float, e.g. 0.2
    """
    app = Flask(__name__)
    df = server.get_client_rates()
    @app.route("/clients/<client_id>", methods=["GET"])
    def get_client_data1(client_id):
        """
        End point for getting client data by client_id.
    
        :param client_id: str
        :return: JSON response
        """
        if client_id in df:
            return jsonify(df[client_id])
        else:
            return jsonify({"error": "Client not found"}), 404

    import requests
    response = requests.get("http://localhost:5000/clients/client1")
    if response.status_code == 200:
        client_data = response.json()
        print("Client Data:", client_data)
        return client_data
    else:
        print("Failed to get client data. Status code:", response.status_code)
    
    # Sample end
# -- TODO END: Part 2


# -- TODO: Part 5, write an API client so we are able to upsert client-rate
def upsert_client_rate(client_id, rate):

    import requests

    # 构建 JSON 数据
    data = {"client_id": client_id, "rate": rate}

    # 发送 HTTP POST 请求来更新或插入客户端利率数据
    response = requests.post("http://127.0.0.1:5000/rate", json=data)

    return response


# -- TODO END: Part 5


# -----------------------Here are tests for API ------------------------
# -------If you want we can any other file call the API functions-------
# -- TODO: Part 3, Test Your API for get rate
# Please add enough testings. Sample:
def test_get_rate():
    print(get_rate('client1'))
    print(get_rate('client2'))
    assert get_rate('client1') == 0.2
    assert get_rate('client0') == 0.0
# -- TODO END: Part 3


# -- TODO: Part 6, Test Your API for upsert client-rate
def test_upsert_rate():
    """
    Test function for upserting client-rate data.
    """
    # 假设这是要测试的客户端 ID 和利率信息
    client_id = "client1"
    rate = 0.2

    # 调用 upsert_client_rate 函数，发送 HTTP POST 请求来更新或插入客户端利率数据
    response = upsert_client_rate(client_id, rate)

    # 打印响应信息
    print("HTTP Status Code:", response.status_code)
    print("Response Content:", response.content)

# 调用测试函数
test_upsert_rate()
# -- TODO END: Part 6


# DO NOT DELETE
if __name__ == '__main__':
    # test_get_rate()
    test_upsert_rate()
    # you can add your test functions here
