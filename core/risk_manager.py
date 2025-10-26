# core/risk_manager.py
# GESTIÓN DE RIESGO: POSICIONES, STOP LOSS, TAKE PROFIT

import time
import logging

class RiskManager:
    def __init__(self):
        self.positions = []

    def add_position(self, symbol, side, entry_price, qty):
        position = {
            'symbol': symbol,
            'side': side,
            'entry': entry_price,
            'qty': qty,
            'timestamp': time.time()
        }
        self.positions.append(position)
        logging.info(f"Posición abierta: {side} {qty} {symbol} @ ${entry_price}")

    def get_positions(self):
        return self.positions

    def remove_position(self, symbol):
        self.positions = [p for p in self.positions if p['symbol'] != symbol]
        logging.info(f"Posición cerrada: {symbol}")

    def check_stop_loss(self, current, entry, side):
        return (side == 'BUY' and current <= entry * 0.985) or (side == 'SELL' and current >= entry * 1.015)

    def check_profit_target(self, current, entry, side):
        return (side == 'BUY' and current >= entry * 1.03) or (side == 'SELL' and current <= entry * 0.97)