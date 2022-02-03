import requests, json, urllib, frappe
@frappe.whitelist()
def mtrhsps(to, message):
	# to ="+254722810063"
	to   = "{}{}".format("+254",to.replace(" ","")[-9:])
	if len(to)!=13: frappe.throw("Invalid Mobile Number") 
	# message = "MTRHSPS Test Bulk SMS. From Salim"
	url = "https://mobilitafrica.com/sms3/messaging/v3/send-sms"
	payload = "to={}&message={}&from=MTRHPENSION&bulkSMSMode=1&keyword=mtrh_pension&tarrif_name=BULK_SMS&campaign_id=10".format(urllib.parse.quote(to),urllib.parse.quote(message))
	# payload = f"""to={to},message={message},bulkSMSMode=1,keyword="mtrh_pension",tarrif_name="BULK_SMS",campaign_id=10&"""

	
	# query =urllib.parse.quote(f"{payload}")

	print(f"{url}?{payload}")

	useless='useless=22'
	headers = {
	'username': 'mtrh_pension',
	'apikey': 'mtrh_pension_2018!',
	'advertiserId': '41',
	'Content-Type': 'application/x-www-form-urlencoded'
	}

	response = requests.request("POST", f"{url}?{payload}", headers=headers, data=useless)

	print(response.text)
# mtrhsps("0722810063","Final test")