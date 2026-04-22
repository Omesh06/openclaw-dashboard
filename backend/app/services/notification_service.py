import requests
import os
from typing import List

class NotificationService:
    def __init__(self):
        # In a real environment, these would be in the config file
        self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TOKEN")
        self.whatsapp_api_key = os.getenv("WHATSAPP_API_KEY", "YOUR_KEY")

    def send_telegram(self, chat_id: str, message: str):
        """Sends a notification to a Telegram chat."""
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        try:
            requests.post(url, json=payload, timeout=5)
            return True
        except Exception as e:
            print(f"Telegram notify error: {e}")
            return False

    def send_whatsapp(self, phone_number: str, message: str):
        """Sends a notification via WhatsApp API."""
        # Mock implementation for the API call
        print(f"[WhatsApp Notification to {phone_number}]: {message}")
        return True

    def dispatch_alert(self, level: str, message: str, recipients: List[Dict]):
        """
        Routes alerts based on level (Urgent/Info).
        recipients: [{"channel": "telegram", "id": "123"}, {"channel": "whatsapp", "id": "456"}]
        """
        prefix = "🚨 URGENT: " if level == "urgent" else "ℹ️ INFO: "
        full_message = f"{prefix}{message}"
        
        for rec in recipients:
            if rec["channel"] == "telegram":
                self.send_telegram(rec["id"], full_message)
            elif rec["channel"] == "whatsapp":
                self.send_whatsapp(rec["id"], full_message)
