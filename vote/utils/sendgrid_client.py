# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
# import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email():
    message = Mail(
        from_email='IEC KMPDU <elections@kmpdu.org>',
        to_emails='railamolo@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return {"success": "email send successfully"}
    except Exception as e:
        print(e.message)
        return {"error": "failed to send email. Error={}".format(e.message)}

send_email()
