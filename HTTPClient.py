import http.client

connection = http.client.HTTPConnection('192.168.0.4:8080')
connection.request("POST", "/data/", body=b'This is my body')
response = connection.getresponse()
headers = response.getheaders()

print('Status: {}\nReason: {}'.format(response.status, response.reason))
##print(str(response.read(),'utf-8'))
##bResponse = response.read().split(b'\n')
sResponse = str(response.read(), 'utf-8')
sResponse = sResponse.split('\n')
print(sResponse)
##print(headers)
connection.close()