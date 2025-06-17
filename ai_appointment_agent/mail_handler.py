import imaplib, smtplib, email
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def get_latest_email():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL, PASSWORD)
    imap.select("inbox")
    _, msgnums = imap.search(None, "UNSEEN")
    msgs = msgnums[0].split()
    if not msgs:
        return "Geen onderwerp", EMAIL, "Geen nieuwe e-mails."
    latest = msgs[-1]
    _, data = imap.fetch(latest, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])
    subject = msg["subject"]
    sender = msg["from"]
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()
    imap.logout()
    return subject, sender, body

def send_email(to_address, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_address
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)
