# -- TODO: Part 2, write an API client so we are able to query
def get_rate(client_id):
    """
    would expect to return a float rate.

    :param client_id: string, e.g. 'client1'
    :return: float, e.g. 0.2
    """
    # Sample code for getting http response. Need to edit
    import requests
    response = requests.get("http://127.0.0.1:5000/rate/" + client_id)
    return response
    # Sample end


# -- TODO END: Part 2


# -- TODO: Part 5, write an API client so we are able to upsert client-rate
def upsert_client_rate(client_id, rate):
    # call http post - http post call to 127.0.0.1:5000/rate
    import requests
    response = requests.post("http://127.0.0.1:5000/rate", json={"client_id": client_id, "client_rate": rate})
    return response
# -- TODO END: Part 5


# -----------------------Here are tests for API ------------------------
# -------If you want we can any other file call the API functions-------
# -- TODO: Part 3, Test Your API for get rate
# Please add enough testings. Sample:
def test_get_rate():
    for i in range(1, 11):
        print(get_rate('client'+str(i)))
    assert get_rate('client1') == 0.2
    assert get_rate("client2") == 0.1
    assert get_rate("client3") == 0.4
    assert get_rate("client4") == 0.05
    assert get_rate("client5") == 0.03
    assert get_rate("client6") == 0.08
    assert get_rate("client7") == 0.3
    assert get_rate("client8") == 0.23
    assert get_rate("client9") == 0.1
    assert get_rate("client10") == 0.1
    assert get_rate('client0') == 0.0


# -- TODO END: Part 3


# -- TODO: Part 6, Test Your API for upsert client-rate
def test_upsert_rate():
    upsert_client_rate("client0", 0.1)
    assert get_rate("client0") == 0.1

    new_rate = get_rate("client1") + 0.1
    upsert_client_rate("client1", new_rate)
    assert get_rate("client1") == new_rate

    upsert_client_rate("client0", 0)
    upsert_client_rate("client1", new_rate - 0.1)
# -- TODO END: Part 6


# DO NOT DELETE
if __name__ == '__main__':
    # test_get_rate()
    test_upsert_rate()
    # you can add your test functions here
