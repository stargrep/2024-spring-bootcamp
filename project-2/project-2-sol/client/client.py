# 与 Flask 应用程序进行通信

# 用于从 Flask 应用程序获取客户的费率信息
def get_rate(client_id):
    """
    would expect to return a float rate.

    :param client_id: string, e.g. 'client1'
    :return: float, e.g. 0.2
    """
    import requests
    response = requests.get("http://127.0.0.1:5000/rate/" + client_id)
    return float(response.content)


"""
这个函数接受一个客户 ID 作为参数，并返回该客户的费率。
它使用了 Python 中的 requests 模块来发送 HTTP GET 请求到 Flask 应用程序的 /rate/<client_id> 路由，以获取客户的费率信息。
请求的 URL 是 http://127.0.0.1:5000/rate/ 加上客户 ID。
函数返回的是 HTTP 响应的内容，需要将其转换为浮点数（因为费率通常是浮点数）
"""


# 用于向 Flask 应用程序更新或插入客户的费率信息
def upsert_client_rate(client_id, rate):
    import requests
    response = requests.post("http://127.0.0.1:5000/rate",
                             json={"client_id": client_id, "rate": rate})


"""
这个函数接受客户 ID 和费率作为参数，并将它们作为 JSON 数据发送到 Flask 应用程序的 /rate 路由，以更新或插入客户的费率信息
它使用了 Python 中的 requests 模块来发送 HTTP POST 请求到 Flask 应用程序的 /rate 路由
请求的 URL 是 http://127.0.0.1:5000/rate
JSON 数据中包含了客户 ID 和费率信息
这个函数没有返回任何内容，因为它主要是用来发送请求并更新服务器端的数据
"""


# -----------------------Here are tests for API ------------------------
def test_upsert_rate():
    #  test create
    upsert_client_rate("client0", 0.1)
    assert get_rate("client0") == 0.1

    #  test update
    new_rate = get_rate("client1") + 0.1
    upsert_client_rate("client1", new_rate)
    assert get_rate("client1") == new_rate

    #  reset
    upsert_client_rate("client0", 0)
    upsert_client_rate("client1", new_rate - 0.1)


if __name__ == '__main__':
    test_upsert_rate()
