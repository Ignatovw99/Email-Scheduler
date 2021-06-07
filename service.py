import database as db
import datetime

import smtplib
import schedule
import _thread
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import email_config

def save_email(subject, content, recipients, email_datetime):

    recipient_ids = db.persist_recipients(recipients)
    email_id = db.persist_email(subject, content, email_datetime)
    db.persist_email_recipients_connection(email_id, recipient_ids)

def build_email_message(email, sender_address):

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ", ".join(list(email.recipients))
    message['Subject'] = email.subject
    message.attach(MIMEText(email.content, 'plain'))
    return message

def send_emails():

    sender_address = email_config["sender_address"]
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, email_config["sender_password"])
    emails_to_send = db.find_emails_by_datetime_with_recipients(datetime.datetime.now())

    for email in emails_to_send:
        email_message = build_email_message(email, sender_address)
        session.sendmail(sender_address, email.recipients, email_message.as_string())

    session.quit()

def setup_schedule_thread():

    schedule.every().minute.at(":00").do(send_emails)

    while True:
        schedule.run_pending()
        time.sleep(1)

def init_schedule_job():
    try:
        _thread.start_new_thread(setup_schedule_thread, ())
    except:
        print("Error: unable to start thread")
