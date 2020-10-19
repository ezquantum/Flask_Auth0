###########test to get bearer token###########
import http.client
print('------------------------test------------------------')
conn = http.client.HTTPSConnection("coffestack.us.auth0.com")

payload = "{\"client_id\":\""+CLIENT_ID_TEST +"\",\"client_secret\":\""+CLIENT_SECRET_TEST+"\",\"audience\":\"blog\",\"grant_type\":\"client_credentials\"}"
headers = {'content-type': "application/json"}

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


#test bearer token - save this token in .env for further api testing:
"""
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilo4YzA4cG1WdVZMTDlGUXlocWUtdiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlc3RhY2sudXMuYXV0aDAuY29tLyIsInN1YiI6IktvSkszWkFOREJVbzNNcVE4OWt1SkRpaEh5b3JXTUhHQGNsaWVudHMiLCJhdWQiOiJibG9nIiwiaWF0IjoxNjAzMDk0OTg2LCJleHAiOjE2MDMxODEzODYsImF6cCI6IktvSkszWkFOREJVbzNNcVE4OWt1SkRpaEh5b3JXTUhHIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOltdfQ.iCmnI1RChSdCY1nr-vv6OFT36XdNZpLTz3nvbp5FSo0W9tLh5JFiwzoNEPoITP8bzigDT0hPqSkmYmlYddZzGDw0XaqKBVate3HKMHqf5Dtn8N12K-m6J8ZmougIKUj2qTwT2SjC_NERV4vQ-5LIR9ftO0fJy2URjw0gHXY0AuLml3KpJz8Y978lxhm2yZI2JqPFbGCyiG1qq-VfzEP9TIJJPJPn0JGin8mmiqERG5r88FTfCo2F0ajyRNejWDKg-9ZqSFrZrJIi2FXptflnwhwZgrSOCbDKQriWF966OZEqfxAopgRcTaCccDv9bV_rDD9pPpyQl7aFnXEJwhCK7Q
"""