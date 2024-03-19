def get_rate(client_id):
    """
    would expect to return a float rate.

    :param client_id: string, e.g. 'client1'
    :return: float, e.g. 0.2
    """
    import requests
    response = requests.get("http://127.0.0.1:5000/rate/" + client_id)
    return response.content
    # Sample end


def upsert_client_rate(client_id, rate):
    import requests
    param = {"client_id": client_id, "rate": rate}
    response = requests.post("http://127.0.0.1:5000/rate", json=param)
    return response.text


# -----------------------Here are tests for API ------------------------
# -------If you want we can any other file call the API functions-------
def test_get_rate():
    response = get_rate('client1')
    assert float(response) == 0.1
    assert float(get_rate('client-1')) == 0


def test_post_rate():
    print(get_rate('client100'))  # should be '0.0'
    upsert_client_rate('client100', 10)
    assert float(get_rate('client100')) == 10


# DO NOT DELETE
if __name__ == '__main__':
    test_get_rate()
    test_post_rate()