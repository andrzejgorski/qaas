import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


url = 'page.url'
sender_email = settings.EMAIL_HOST
host = settings.SMTP_HOST
port = settings.SMTP_PORT or None
login = settings.SMTP_LOGIN or None
password = settings.SMTP_PASSWORD or None


def _send_message(msg):
    server = smtplib.SMTP(host, port)
    if login and password:
        server.login(login, password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    print(msg)
    server.quit()


def send_invitations(email_objects, quiz):
    msg = MIMEMultipart()
    msg['Subject'] = f'Invitation to quiz: {quiz.name}'
    msg['From'] = sender_email
    recipients = ', '.join((obj.email for obj in email_objects)) 
    msg['To'] = recipients
    msg.attach(MIMEText(f'Invitation to the quiz: {quiz.name}. If you want to join visit: {url}'))
    _send_message(msg)


def notify_through_email(message_body, participation):
    msg = MIMEMultipart()
    msg['Subject'] = f"{participation.quiz.name} Quiz Result"
    msg['From'] = sender_email
    msg['To'] = participation.user.email
    msg.attach(MIMEText(message_body))
    _send_message(msg)
