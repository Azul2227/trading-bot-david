# config/settings.py
import json
import logging

class Settings:
    def __init__(self):
        try:
            with open('config/settings.json') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            logging.warning("settings.json no encontrado. Usando valores por defecto.")
            self.data = {
                "max_risk_per_trade_percent": 0.10,
                "operation_time_limit_minutes": 5,
                "telegram_token": "TU_TOKEN"
            }

    def get(self, key, default=None):
        return self.data.get(key, default)