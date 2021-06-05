import database as db

def save_email(subject, content, recipients, email_datetime):

    recipient_ids = db.persist_recipients(recipients)
    email_id = db.persist_email(subject, content, email_datetime)
    db.persist_email_recipients_connection(email_id, recipient_ids)

