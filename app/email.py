from flask_mail import Message, Mail
from flask import current_app
import logging

logger = logging.getLogger(__name__)
mail = Mail()

def send_email(subject, recipients, html_body):
    app = current_app._get_current_object()
    msg = Message(subject, recipients=recipients, html=html_body)
    logger.debug(f"Preparing to send email with subject '{subject}' to {recipients}")

    try:
        with app.app_context():
            mail = current_app.extensions['mail']
            logger.debug(f"Sending email to {msg.recipients}")
            mail.send(msg)
            logger.info(f"Email sent to {msg.recipients}")
            return "Success"
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return f"Failed: {e}"