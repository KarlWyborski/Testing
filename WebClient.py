import http.client

connection = http.client.HTTPSConnection('http://192.168.0.4:8080')
connection.request('GET','/')
response = connection.getresponse()
print('Status: {}\nReason: {}'.format(response.status, response.reason))

connection.close()