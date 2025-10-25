# main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.bot import TradingBot
from exchanges.paypal import PayPalP2P

if __name__ == "__main__":
    print("Iniciando bot en modo LIVE + PayPal P2P...")
    
    try:
        paypal = PayPalP2P()
        print("PayPal P2P configurado correctamente")
    except Exception as e:
        print(f"Error PayPal: {e}")

    bot = TradingBot()
    try:
        bot.start()
    except KeyboardInterrupt:
        print("\nDeteniendo bot...")
        bot.stop()