def get_rate(client_id):
    """
    would expect to return a float rate.

    :param client_id: string, e.g. 'client1'
    :return: float, e.g. 0.2
    """
    # Sample code for getting http response. Need to edit
    import requests
    response = requests.get("http://127.0.0.1:5000/rate/" + client_id)
    return response.content


def upsert_client_rate(client_id, rate):
    import requests
    # call http post - http post call to 127.0.0.1:5000/rate
    param = {"client_id": client_id, "rate": rate}
    response = requests.post("http://127.0.0.1:5000/rate", json=param)
    return response.text


# -----------------------Here are tests for API ------------------------
def test_get_rate():
    response = get_rate('client1')
    assert float(response) == 0.2


def test_post_rate():
    print(get_rate('client100'))  # should be 'NOT FOUND'
    # if we add this client already, then will not be NOT FOUND
    upsert_client_rate('client100', 10)
    assert float(get_rate('client100')) == 10


if __name__ == '__main__':
    test_get_rate()
    test_post_rate()
