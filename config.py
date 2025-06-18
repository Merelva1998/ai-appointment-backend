"""
Configuratie instellingen voor de AI Appointment Assistant
"""

import os
from dotenv import load_dotenv

# Laad environment variables
load_dotenv()

# Email configuratie
EMAIL_CONFIG = {
    'address': os.getenv('EMAIL_ADDRESS'),
    'password': os.getenv('EMAIL_PASSWORD'),
    'imap_server': os.getenv('IMAP_SERVER', 'imap.gmail.com'),
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'imap_port': int(os.getenv('IMAP_PORT', '993')),
    'smtp_port': int(os.getenv('SMTP_PORT', '587'))
}

# OpenAI configuratie
OPENAI_CONFIG = {
    'api_key': os.getenv('OPENAI_API_KEY'),
    'model': 'gpt-4o',  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
    'max_tokens': 1000,
    'temperature': 0.7
}

# Applicatie configuratie
APP_CONFIG = {
    'check_interval': int(os.getenv('CHECK_INTERVAL', '30')),  # seconden tussen email checks
    'max_emails_per_check': int(os.getenv('MAX_EMAILS_PER_CHECK', '10')),
    'business_hours_start': int(os.getenv('BUSINESS_HOURS_START', '9')),
    'business_hours_end': int(os.getenv('BUSINESS_HOURS_END', '17')),
    'default_appointment_duration': int(os.getenv('DEFAULT_APPOINTMENT_DURATION', '60')),  # minuten
    'timezone': os.getenv('TIMEZONE', 'Europe/Amsterdam')
}

# Logging configuratie
LOGGING_CONFIG = {
    'log_file': os.getenv('LOG_FILE', 'appointment_assistant.log'),
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    'log_to_console': os.getenv('LOG_TO_CONSOLE', 'true').lower() == 'true',
    'log_to_file': os.getenv('LOG_TO_FILE', 'true').lower() == 'true'
}

def validate_config():
    """Valideer of alle vereiste configuratie aanwezig is"""
    errors = []
    
    if not EMAIL_CONFIG['address']:
        errors.append("EMAIL_ADDRESS is niet geconfigureerd")
    
    if not EMAIL_CONFIG['password']:
        errors.append("EMAIL_PASSWORD is niet geconfigureerd")
    
    if not OPENAI_CONFIG['api_key']:
        errors.append("OPENAI_API_KEY is niet geconfigureerd")
    
    return errors
