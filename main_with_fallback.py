import os
import time
from dotenv import load_dotenv
from ai_appointment_agent.mail_handler import EmailHandler
from ai_appointment_agent.agent import AppointmentAgent
from ai_appointment_agent.appointment_manager import AppointmentManager
from ai_appointment_agent.logger import Logger
from ai_appointment_agent.user_manager import UserManager

# Load environment variables
load_dotenv()

class FallbackAppointmentAgent:
    """Fallback agent when OpenAI API is not available"""
    
    def __init__(self, appointment_manager):
        self.appointment_manager = appointment_manager
        self.user_manager = UserManager()
    
    def generate_response(self, subject, body, sender_email):
        """Generate simple response without AI"""
        # Check subscription status first
        if not self.user_manager.is_subscription_active():
            return {
                'response': "Sorry, uw abonnement is verlopen. Neem contact op om uw account te verlengen.",
                'subscription_expired': True
            }
        
        # Simple keyword detection for appointment requests
        appointment_keywords = ['afspraak', 'appointment', 'meeting', 'plan', 'datum', 'tijd', 'wanneer']
        
        subject_lower = subject.lower()
        body_lower = body.lower()
        
        # Check if it looks like an appointment request
        is_appointment_request = any(keyword in subject_lower or keyword in body_lower 
                                   for keyword in appointment_keywords)
        
        if is_appointment_request:
            # Get custom response or use default
            custom_response = self.user_manager.get_custom_response('confirmation')
            office_hours = self.user_manager.get_setting('office_hours', {})
            
            response = f"""Bedankt voor uw afspraakverzoek!

Ik ben Merel's AI Appointment Assistant. Om uw afspraak in te plannen, heb ik de volgende informatie nodig:

• Gewenste datum en tijd
• Doel van de afspraak  
• Geschatte duur
• Eventuele locatievoorkeur

Kantooruren: {office_hours.get('start', 9)}:00 - {office_hours.get('end', 17)}:00
Werkdagen: {', '.join(office_hours.get('days', ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag']))}

U kunt mij een nieuwe email sturen met deze details, bijvoorbeeld:
"Ik wil graag een afspraak plannen op maandag 24 juni om 14:00 voor een consult van 1 uur."

Met vriendelijke groet,
AI Appointment Assistant"""
        else:
            response = f"""Bedankt voor uw bericht!

Ik ben Merel's AI Appointment Assistant en ben gespecialiseerd in het plannen van afspraken.

Als u een afspraak wilt maken, stuur dan een email met:
• Gewenste datum en tijd
• Doel van de afspraak
• Geschatte duur

Voor andere vragen kunt u direct contact opnemen.

Met vriendelijke groet,
AI Appointment Assistant"""
        
        return {
            'response': response,
            'appointment_details': None,
            'has_conflicts': False
        }

def main():
    """Main function with fallback handling"""
    logger = Logger()
    logger.log("AI Appointment Assistant gestart (met fallback functionaliteit)...")
    
    try:
        # Initialize components
        email_handler = EmailHandler()
        appointment_manager = AppointmentManager()
        
        # Try to use AI agent first, fallback if needed
        try:
            agent = AppointmentAgent(appointment_manager)
            logger.log("AI agent geïnitialiseerd")
        except Exception as e:
            logger.log(f"AI agent niet beschikbaar, gebruik fallback: {str(e)}")
            agent = FallbackAppointmentAgent(appointment_manager)
        
        logger.log("Alle componenten succesvol geïnitialiseerd")
        
        # Check for email credentials
        if not email_handler.credentials_valid():
            logger.log("FOUT: Email credentials zijn niet correct geconfigureerd.")
            return
        
        # Main processing loop
        logger.log("Start email monitoring...")
        
        while True:
            try:
                # Get unread emails
                unread_emails = email_handler.get_unread_emails()
                
                if unread_emails:
                    logger.log(f"{len(unread_emails)} nieuwe email(s) gevonden")
                    
                    for email_data in unread_emails:
                        process_email_safe(email_data, agent, email_handler, logger)
                else:
                    logger.log("Geen nieuwe emails gevonden")
                
                # Wait before checking again
                time.sleep(int(os.getenv("CHECK_INTERVAL", "30")))
                
            except KeyboardInterrupt:
                logger.log("Applicatie gestopt door gebruiker")
                break
            except Exception as e:
                logger.log(f"FOUT tijdens email monitoring: {str(e)}")
                time.sleep(60)
                
    except Exception as e:
        logger.log(f"KRITIEKE FOUT: {str(e)}")

def process_email_safe(email_data, agent, email_handler, logger):
    """Process email with error handling"""
    try:
        subject = email_data.get('subject', '')
        sender = email_data.get('sender', '')
        body = email_data.get('body', '')
        message_id = email_data.get('message_id', '')
        
        logger.log(f"Verwerken email van {sender}: {subject}")
        
        # Generate response with fallback handling
        try:
            response_data = agent.generate_response(subject, body, sender)
        except Exception as api_error:
            logger.log(f"AI API fout, gebruik fallback: {str(api_error)}")
            # Use fallback agent
            if hasattr(agent, 'appointment_manager'):
                fallback_agent = FallbackAppointmentAgent(agent.appointment_manager)
            else:
                fallback_agent = FallbackAppointmentAgent(AppointmentManager())
            response_data = fallback_agent.generate_response(subject, body, sender)
        
        if response_data and response_data.get('response'):
            # Send reply
            success = email_handler.send_reply(
                to_email=sender,
                subject=f"Re: {subject}",
                body=response_data['response'],
                original_message_id=message_id
            )
            
            if success:
                logger.log(f"Antwoord verzonden naar {sender}")
                email_handler.mark_as_read(message_id)
            else:
                logger.log(f"FOUT: Kon antwoord niet verzenden naar {sender}")
        else:
            logger.log(f"Geen antwoord gegenereerd voor email van {sender}")
            
    except Exception as e:
        logger.log(f"FOUT tijdens verwerken email: {str(e)}")

if __name__ == "__main__":
    main()