# config/settings.py
# CONFIGURACIÓN GLOBAL DEL BOT

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
                "profit_target_percent": 3.0,
                "stop_loss_percent": 1.5,
                "telegram_token": "TU_TOKEN_TELEGRAM"
            }

    def get(self, key, default=None):
        return self.data.get(key, default)