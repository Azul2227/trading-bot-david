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
            if balance < 10:
                self.paypal.buy_crypto(10)
                self.notifier.send("Recarga automática: 10 USD vía PayPal P2P")
                time.sleep(60)
                balance = self.bitso.get_balance()

            risk_amount = balance * 0.10
            price_data = self.bitso.get_symbol_ticker(symbol)
            price = float(price_data['price'])
            qty = risk_amount / price
            qty = round(qty, 6)

            logging.info(f"OPERANDO: {side} {qty} {symbol} a ${price}")
            order = self.bitso.place_order(symbol, side, qty)
            if order:
                self.risk.add_position(symbol, side, price, qty)
                self.notifier.send(f"COMPRA: {qty} {symbol} a ${price}")

        except Exception as e:
            logging.error(f"Error en trade: {e}")

    def check_positions(self):
        positions = self.risk.get_positions()
        for pos in positions:
            current = float(self.bitso.get_symbol_ticker(pos['symbol'])['price'])
            if self.risk.check_stop_loss(current, pos['entry'], pos['side']):
                self.close_position(pos, current, "STOP LOSS")
            elif self.risk.check_profit_target(current, pos['entry'], pos['side']):
                self.close_position(pos, current, "TAKE PROFIT")

    def close_position(self, pos, price, reason):
        side = 'SELL' if pos['side'] == 'BUY' else 'BUY'
        order = self.bitso.place_order(pos['symbol'], side, pos['qty'])
        if order:
            pnl = (price - pos['entry']) * pos['qty'] if pos['side'] == 'BUY' else (pos['entry'] - price) * pos['qty']
            self.risk.remove_position(pos['symbol'])
            self.notifier.send(f"{reason}: {side} {pos['qty']} {pos['symbol']} | PnL: {pnl:.2f} USD")