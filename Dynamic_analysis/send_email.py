# send_email.py

import smtplib
import ssl
from email.message import EmailMessage

def send_email(error):
    port = 465
    password = "hmpslrbqxjadacee"
    context = ssl.create_default_context()

    msg = EmailMessage()
    msg['Subject'] = 'Dynamic testing report'
    msg['From'] = 'ruoxisun278@gmail.com'
    msg['To'] = 'ruoxisun278@gmail.com'
    msg.set_content(error)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("ruoxisun278@gmail.com", password)
        server.send_message(msg)