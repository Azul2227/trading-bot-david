# core/risk_manager.py
import time
import logging

class RiskManager:
    def __init__(self):
        self.positions = []  # Lista de posiciones abiertas

    def add_position(self, symbol, side, entry_price, qty):
        """Añade una posición"""
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
        """Devuelve todas las posiciones abiertas"""
        return self.positions

    def remove_position(self, symbol):
        """Elimina una posición por símbolo"""
        self.positions = [p for p in self.positions if p['symbol'] != symbol]
        logging.info(f"Posición cerrada: {symbol}")

    def check_stop_loss(self, current_price, entry_price, side):
        """Stop Loss: 1.5%"""
        if side == 'BUY':
            return current_price <= entry_price * 0.985
        else:
            return current_price >= entry_price * 1.015

    def check_profit_target(self, current_price, entry_price, side):
        """Take Profit: 3%"""
        if side == 'BUY':
            return current_price >= entry_price * 1.03
        else:
            return current_price <= entry_price * 0.97