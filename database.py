import mysql.connector

from util import convert_datetime_to_string

def execute(func, *args):
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1234qwer",
            database = "email_scheduler"
        )
        cursor = connection.cursor()
        result = func(cursor, *args)
        connection.commit()
        cursor.close()
        connection.close()
        return result
    except:
        print("Database error")

def insert(mysql_cursor, table, columns, values):
    value_placeholder = ", ".join(["%s" for _ in range(len(values))])
    column_names = ", ".join(columns)
    query = f"INSERT INTO {table}({column_names}) VALUES({value_placeholder})"
    mysql_cursor.execute(query, values)
    return mysql_cursor.lastrowid

def find_by_query(mysql_cursor, query):
    mysql_cursor.execute(query)
    return mysql_cursor.fetchall()

def find(mysql_cursor, table, columns, condition):

    column_names = "*" if columns is None or len(columns) == 0 else ", ".join(columns)
    query = f"SELECT {column_names} FROM {table}"
    if condition is not None:
        query = query + f" WHERE {condition}"
    mysql_cursor.execute(query)

def find_one(mysql_cursor, table, columns, condition):
    find(mysql_cursor, table, columns, condition)
    return mysql_cursor.fetchone()
    
def find_all(mysql_cursor, table, columns, condition):
    find(mysql_cursor, table, columns, condition)
    return mysql_cursor.fetchall()

def persist_recipients(recipients):
    
    recipient_ids = []

    for current_address in recipients:
        recipient_candidate = execute(find_one, "recipients", None, f"address = '{current_address}'")
        exist_already = recipient_candidate is not None
        current_id = None
        if exist_already == False:
            id = execute(insert, "recipients", ["address"], [current_address])
            current_id = id
        else:
            current_id = recipient_candidate[0]

        recipient_ids.append(current_id)

    return recipient_ids

def persist_email(subject, content, email_datetime):
    
    columns = ["subject", "content", "datetime"]
    values = [subject, content, email_datetime]
    return execute(insert, "emails", columns, values)

def persist_email_recipients_connection(email_id, recipient_ids):
    columns = ["email_id", "recipient_id"]
    for recipient_id in recipient_ids:
        execute(insert, "emails_recipients", columns, [email_id, recipient_id])

class Email:

    def __init__(self, id, subject, content, send_datetime, recipients):

        self.id = id
        self.subject = subject
        self.content = content
        self.send_datetime = send_datetime
        self.recipients = recipients

def find_emails_by_datetime_with_recipients(email_datetime):

    result = []
    emails = execute(find_all, "emails", None, f"datetime = '{convert_datetime_to_string(email_datetime)}'")
    
    recipients_email_query_template = (
                "SELECT r.address FROM recipients AS r "
                + "JOIN emails_recipients AS er ON r.id = er.recipient_id WHERE er.email_id = "
    )

    for email in emails:
        id = email[0]
        current_recipients_query = recipients_email_query_template + str(id)
        recipients_result = execute(find_by_query, current_recipients_query)
        recipients = list(map(lambda recipient: recipient[0], recipients_result))
        email_obj = Email(*email, recipients)
        result.append(email_obj)

    return result
