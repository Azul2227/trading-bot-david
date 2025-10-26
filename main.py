# main.py
import logging
from core.bot import TradingBot
from utils.logger import setup_logger

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Iniciando bot en modo LIVE + PayPal P2P...")
    print("Iniciando bot en modo LIVE + PayPal P2P...")
    
    bot = TradingBot()
    bot.start()