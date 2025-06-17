
from mail_handler import get_latest_email
from agent import generate_reply

print("🤖 AI Appointment Assistant gestart...")

subject, sender, body = get_latest_email()

if subject and sender and body:
    print(f"📩 Nieuwe e-mail van {sender}: {subject}")
    reply = generate_reply(body)
    print("🤖 Antwoord gegenereerd:")
    print(reply)
else:
    print("📭 Geen nieuwe e-mails gevonden.")
