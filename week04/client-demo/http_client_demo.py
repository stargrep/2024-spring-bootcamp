import http.client

connection = http.client.HTTPConnection("localhost:5000")
connection.request("GET", "/hello")
response = connection.getresponse()
print("Status: {} and reason: {}".format(response.status, response))

connection.close()
