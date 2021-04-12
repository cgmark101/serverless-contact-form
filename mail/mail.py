import email
import smtplib
from datetime import datetime

def sender():
    now = datetime.now()
    gmail_user = 'example@gmail.com'
    gmail_password = 'zmssnqhpzloffnbsert4'

    message = """
    You have received a contact
    Check your database
    """
    msg = email.message_from_string(message)
    msg['From'] = "example@gmail.com"
    msg['To'] = "example2@gmail.com"
    msg['Subject'] = f"{now}"

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo() 
    s.login(gmail_user, gmail_password)
    s.sendmail(gmail_user, "example2@gmail.com", msg.as_string())

    s.close()
