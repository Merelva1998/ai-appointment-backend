
import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv()

def get_latest_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
    mail.select("inbox")

    result, data = mail.search(None, "UNSEEN")
    ids = data[0].split()
    if not ids:
        return None, None, None

    latest_id = ids[-1]
    result, data = mail.fetch(latest_id, "(RFC822)")
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    subject = msg["subject"]
    sender = msg["from"]

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    return subject, sender, body
