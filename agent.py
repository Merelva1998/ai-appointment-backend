
import os
import requests
import json
from dotenv import load_dotenv
from config import USE_WHITELABEL

load_dotenv()

def generate_reply(user_message):
    system_prompt = (
        "Je bent een informele, vriendelijke assistent van een ondernemer. "
        "Jouw taak is het beantwoorden van e-mails over afspraken. Stel maximaal twee momenten voor. "
        "Houd het kort, behulpzaam en menselijk."
    )
    if not USE_WHITELABEL:
        system_prompt += "\n\nAutomatisch verstuurd via de AI Appointment Assistant van Merel VA."

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=body,
        headers=headers
    )
    return response.json()["choices"][0]["message"]["content"]
