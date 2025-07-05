import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage

def email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "org.imj.yyc@gmail.com"
    password = "xxx"

    recipient_email = "imjogiat@gmail.com" 

    context= ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as mailserver:
        mailserver.login(user=username, password=password)
        mailserver.send_message(message, username, recipient_email)
        
