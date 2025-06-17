from mail_handler import get_latest_email, send_email
from agent import generate_reply

if __name__ == "__main__":
    print("🧠 AI Appointment Assistant gestart...")
    subject, sender, body = get_latest_email()
    print(f"📩 Nieuwe e-mail van {sender}: {subject}")
    ai_reply = generate_reply(body)
    send_email(to_address=sender, subject=f"Re: {subject}", body=ai_reply)
