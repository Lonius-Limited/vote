import requests
import json
def get_msg():
	return f"<div><h3>Hello, just to confirm earlier invoice</h3></div>"
def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/email.dalasystems.com/messages",
		auth=("api", "4021f0585c350e90ff563fce35e29f3d-71b35d7e-e9e3edbd"),
		data={"from": "IEC KMPDU <mailgun@email.dalasystems.com>",
			"to": ["dsmwaura@gmail.com","railamolo@gmail.com"],
			"subject": "Hello Guy",
			"html": get_msg()})
p = send_simple_message()
print(p.text)