import json
import requests

user_name = input ("Enter name of the user :")


print(user_name+' currently has these privileges for the session')
user_request_dict = {
	"User": user_name,
}
jsonData = json.dumps(user_request_dict)

response = requests.post('http://127.0.0.1:5000/test', json=jsonData)

print("Status code: ", response.status_code)
print("Printing Entire Post Request")
print(response.json())