# utils/notifier.py
# ENVÍA NOTIFICACIONES A TELEGRAM

import logging

class TelegramNotifier:
    def __init__(self, token):
        self.token = token

    def send(self, msg):
        logging.info(f"Telegram: {msg}")