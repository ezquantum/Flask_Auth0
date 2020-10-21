import http.client

conn = http.client.HTTPSConnection("coffestack.us.auth0.com")

payload = "{\"client_id\":\"KoJK3ZANDBUo3MqQ89kuJDihHyorWMHG\",\"client_secret\":\"KdhzQGTwrFongHpHutXt40YPKTi5CmIqeQ0bVgR54UvlvMPTrucW7SsCmSo1loSp\",\"audience\":\"blog\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))