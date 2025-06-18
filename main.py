import os
import time
from dotenv import load_dotenv
from ai_appointment_agent.mail_handler import EmailHandler
from ai_appointment_agent.agent import AppointmentAgent
from ai_appointment_agent.appointment_manager import AppointmentManager
from ai_appointment_agent.logger import Logger

# Load environment variables
load_dotenv()

def main():
    """Main function to run the AI Appointment Assistant"""
    logger = Logger()
    logger.log("AI Appointment Assistant gestart...")
    
    try:
        # Initialize components
        email_handler = EmailHandler()
        appointment_manager = AppointmentManager()
        agent = AppointmentAgent(appointment_manager)
        
        logger.log("Alle componenten succesvol geïnitialiseerd")
        
        # Check for email credentials
        if not email_handler.credentials_valid():
            logger.log("FOUT: Email credentials zijn niet correct geconfigureerd. Controleer .env bestand.")
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
                        process_email(email_data, agent, email_handler, logger)
                else:
                    logger.log("Geen nieuwe emails gevonden")
                
                # Wait before checking again (configurable interval)
                time.sleep(int(os.getenv("CHECK_INTERVAL", "30")))
                
            except KeyboardInterrupt:
                logger.log("Applicatie gestopt door gebruiker")
                break
            except Exception as e:
                logger.log(f"FOUT tijdens email monitoring: {str(e)}")
                time.sleep(60)  # Wait longer on error
                
    except Exception as e:
        logger.log(f"KRITIEKE FOUT: {str(e)}")

def process_email(email_data, agent, email_handler, logger):
    """Process a single email and send response"""
    try:
        subject = email_data.get('subject', '')
        sender = email_data.get('sender', '')
        body = email_data.get('body', '')
        message_id = email_data.get('message_id', '')
        
        logger.log(f"Verwerken email van {sender}: {subject}")
        
        # Generate AI response
        response_data = agent.generate_response(subject, body, sender)
        
        if response_data:
            # Send reply
            success = email_handler.send_reply(
                to_email=sender,
                subject=f"Re: {subject}",
                body=response_data['response'],
                original_message_id=message_id
            )
            
            if success:
                logger.log(f"Antwoord verzonden naar {sender}")
                # Mark email as processed
                email_handler.mark_as_read(message_id)
            else:
                logger.log(f"FOUT: Kon antwoord niet verzenden naar {sender}")
        else:
            logger.log(f"Geen antwoord gegenereerd voor email van {sender}")
            
    except Exception as e:
        logger.log(f"FOUT tijdens verwerken email: {str(e)}")

if __name__ == "__main__":
    main()
