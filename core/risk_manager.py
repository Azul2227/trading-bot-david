import time
import json
from datetime import datetime, timedelta
import logging
import random


class RiskManager:
    def __init__(self):
        try:
            with open('config/settings.json') as f:
                self.config = json.load(f)
        except:
            self.config = {}
        self.start_time = datetime.now()
        self.positions = []

    def should_close_early(self):
        if not self.config:
            return False
        elapsed = (datetime.now() - self.start_time).total_seconds() / 60
        limit = self.config.get('operation_time_limit_minutes', 30)
        return elapsed >= (limit - self.config.get('close_before_minutes', 2))

    def add_position(self, symbol, side, entry_price, qty):
        self.positions.append({
            'symbol': symbol,
            'side': side,
            'entry': entry_price,
            'qty': qty,
            'time': datetime.now()
        })
        logging.info(f"Posición abierta: {side} {qty} {symbol} @ {entry_price}")

    def check_profit_target(self, current_price, entry, side):
        if side == 'BUY':
            profit = (current_price - entry) / entry
        else:
            profit = (entry - current_price) / entry
        return profit >= 0.03  # 3% ganancia
    
    def get_volatility(self):
        # Simulación: 1% = bajo, 5% = alto
        return random.uniform(1, 5)
    
    def check_stop_loss(self, current_price, entry, side):
        if side == 'BUY':
            loss = (entry - current_price) / entry
        else:
            loss = (current_price - entry) / entry
        return loss >= 0.015  # 1.5% pérdida