import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email():
    message = Mail(
        from_email='election@kmpdu.org',
        to_emails='railamolo@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)