# core/trader.py
from exchanges.bitso import BitsoTraderimport
import logging
from utils.notifier import TelegramNotifier, EmailNotifier
from exchanges.paypal import PayPalP2P
import time

class Trader:
    def __init__(self):
        self.paypal = PayPalP2P()
        self.bitso = BitsoTrader()        
        self.risk = RiskManager()
        self.notifier = TelegramNotifier("8103459177:AAF54aPjAKBrhxfkP2pmur_Ajjc3c8qONOE")
        try:
            with open('config/settings.json') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            logging.error("config/settings.json no encontrado")
            self.config = {}

    def execute_trade(self, symbol, side):
        try:
            balance = self.bitso.get_bitso()
            if balance <= 0:
                logging.warning("Saldo insuficiente para operar")
                return
            
            # RECARGA CON PAYPAL SI SALDO < 10 USDT
            if balance < 10:
                self.paypal.buy_crypto(10)
                self.notifier.send("Fondos bajos: Comprando 10 USD vía PayPal P2P")
                time.sleep(60)
                balance = self.bitso.get_bitso()  # Actualiza saldo

            # === 10% DEL SALDO TOTAL ===
            max_risk_percent = self.config.get('max_risk_per_trade_percent', 0.10)
            risk_amount = balance * max_risk_percent  # ¡10% del saldo total!

            price_data = self.bitso.client.get_symbol_ticker(symbol=symbol)
            price = float(price_data['price'])
            qty = risk_amount / price
            qty = round(qty, 6)

            print(f"OPERANDO: {side} {qty} {symbol} a ${price} | Riesgo: {risk_amount:.2f} USDT ({max_risk_percent*100}%)")
            logging.info(f"Orden: {side} {qty} {symbol}")

            # Simulación (en LIVE será orden real)
            self.risk.add_position(symbol, side, price, qty)

            # Notificación
            self.notifier.send(f"COMPRA: {qty} {symbol} a ${price}\nRiesgo: {risk_amount:.2f} USDT ({max_risk_percent*100}%)")

        except Exception as e:
            logging.error(f"Error en execute_trade: {e}")
    def check_positions(self):
        if self.risk.should_close_early():
            print("CERRANDO TODAS LAS POSICIONES: Límite de tiempo")
            self.close_all("Límite de tiempo")
            return

        for pos in self.risk.positions[:]:
            try:
                current_price = float(self.binance.client.get_symbol_ticker(symbol=pos['symbol'])['price'])
                
                # STOP LOSS
                if self.risk.check_stop_loss(current_price, pos['entry'], pos['side']):
                    opposite = 'SELL' if pos['side'] == 'BUY' else 'BUY'
                    print(f"STOP LOSS: {opposite} {pos['qty']} {pos['symbol']}")
                    self.risk.positions.remove(pos)
                    continue

                # TAKE PROFIT
                if self.risk.check_profit_target(current_price, pos['entry'], pos['side']):
                    opposite = 'SELL' if pos['side'] == 'BUY' else 'BUY'
                    print(f"TAKE PROFIT: {opposite} {pos['qty']} {pos['symbol']}")
                    self.risk.positions.remove(pos)
            except Exception as e:
                logging.error(f"Error check_positions: {e}")

    def close_all(self, reason):
        print(f"CERRANDO TODO: {reason}")
        self.risk.positions.clear()
