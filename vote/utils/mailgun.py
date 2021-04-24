import requests
import json
def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/email.dalasystems.com",
		auth=("api", "4021f0585c350e90ff563fce35e29f3d-71b35d7e-e9e3edbd"),
		data={"from": "Excited User <mailgun@email.dalasystems.com>",
			"to": ["dsmwaura@gmail.com","railamolo@gmail.com"],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})
p = send_simple_message()
print(p.content)
