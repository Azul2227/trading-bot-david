# core/trader.py
import logging
import time
from exchanges.bitso import BitsoTrader
from core.risk_manager import RiskManager
from utils.paypal import PayPalP2P
from utils.notifier import TelegramNotifier
from config.settings import Settings

class Trader:
    def __init__(self):
        self.config = Settings()
        self.bitso = BitsoTrader()
        self.paypal = PayPalP2P()
        self.risk = RiskManager()
        self.notifier = TelegramNotifier(self.config.get('telegram_token'))

    def execute_trade(self, symbol, side):
        try:
            balance = self.bitso.get_balance()
            if balance <= 0:
                logging.warning("Saldo insuficiente para operar")
                return

            # RECARGA AUTOMÁTICA CON PAYPAL P2P SI SALDO < 10 USD
            if balance < 10:
                self.paypal.buy_crypto(10)
                self.notifier.send("Fondos bajos: Recargando 10 USD vía PayPal P2P")
                time.sleep(60)
                balance = self.bitso.get_balance()

            # === RIESGO MÁXIMO 10% DEL SALDO TOTAL ===
            max_risk_percent = self.config.get('max_risk_per_trade_percent', 0.10)
            risk_amount = balance * max_risk_percent

            price_data = self.bitso.get_symbol_ticker(symbol)
            price = float(price_data['price'])
            qty = risk_amount / price
            qty = round(qty, 6)

            print(f"OPERANDO EN BITSO: {side} {qty} {symbol} a ${price} | Riesgo: {risk_amount:.2f} USD ({max_risk_percent*100}%)")
            logging.info(f"Orden: {side} {qty} {symbol}")

            # ORDEN REAL EN BITSO
            order = self.bitso.place_order(symbol, side, qty)
            if order:
                self.risk.add_position(symbol, side, price, qty)
                self.notifier.send(f"COMPRA: {qty} {symbol} a ${price}\nRiesgo: {risk_amount:.2f} USD")

        except Exception as e:
            logging.error(f"Error en execute_trade: {e}")

    def check_positions(self):
        positions = self.risk.get_positions()
        for pos in positions:
            current_price_data = self.bitso.get_symbol_ticker(pos['symbol'])
            current_price = float(current_price_data['price'])

            # STOP LOSS (1.5%)
            if self.risk.check_stop_loss(current_price, pos['entry'], pos['side']):
                self.close_position(pos, current_price, "STOP LOSS")
                continue

            # TAKE PROFIT (3%)
            if self.risk.check_profit_target(current_price, pos['entry'], pos['side']):
                self.close_position(pos, current_price, "TAKE PROFIT")
                continue

            # CIERRE POR TIEMPO (2 min antes del límite)
            if time.time() - pos['timestamp'] > (self.config.get('operation_time_limit_minutes', 5) - 1) * 60:
                self.close_position(pos, current_price, "LÍMITE DE TIEMPO")

    def close_position(self, pos, current_price, reason):
        try:
            side = 'SELL' if pos['side'] == 'BUY' else 'BUY'
            order = self.bitso.place_order(pos['symbol'], side, pos['qty'])
            if order:
                pnl = (current_price - pos['entry']) * pos['qty'] if pos['side'] == 'BUY' else (pos['entry'] - current_price) * pos['qty']
                self.risk.remove_position(pos['symbol'])
                self.notifier.send(f"{reason}: {side} {pos['qty']} {pos['symbol']} a ${current_price}\nPnL: {pnl:.2f} USD")
                logging.info(f"Posición cerrada: {reason} | PnL: {pnl:.2f}")
        except Exception as e:
            logging.error(f"Error cerrando posición: {e}")