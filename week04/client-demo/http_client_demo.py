import http.client

connection = http.client.HTTPConnection("localhost:8003")
connection.request("GET", "/")
response = connection.getresponse()
print("Status: {} and reason: {}".format(response.status, response))

connection.close()