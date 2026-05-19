"""Notifications Module"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from telegram import Bot
except ImportError:
    Bot = None

logger = logging.getLogger(__name__)


class NotificationManager:
    """Handle all notifications"""

    def __init__(self, config):
        self.config = config
        self.email_enabled = config["notifications"]["email"]["enabled"]
        self.telegram_enabled = config["notifications"]["telegram"]["enabled"]

    def send_notification(self, subject, message, details=""):
        """Send notification via all enabled channels"""
        full_message = f"{subject}\n{message}\n\n{details}"

        if self.email_enabled:
            self.send_email(subject, full_message)

        if self.telegram_enabled:
            self.send_telegram(full_message)

        logger.info(f"Notification sent: {subject}")

    def send_email(self, subject, message):
        """Send email notification"""
        try:
            config = self.config["notifications"]["email"]
            sender = config["sender"]
            password = config["password"]
            recipients = config["recipients"]

            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = f"[Trading Bot] {subject}"
            msg.attach(MIMEText(message, "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()

            logger.info(f"Email sent: {subject}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    def send_telegram(self, message):
        """Send Telegram notification"""
        if Bot is None:
            logger.warning("Telegram bot not available")
            return

        try:
            config = self.config["notifications"]["telegram"]
            token = config["token"]
            chat_id = config["chat_id"]

            bot = Bot(token=token)
            bot.send_message(chat_id=chat_id, text=message)
            logger.info("Telegram message sent")
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
