# core/bot.py
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from core.trader import Trader
from core.market_research import MarketResearch
from exchanges.bitso import BitsoTrader
from utils.paypal import PayPalP2P
from config.settings import Settings
from utils.logger import setup_logger

class TradingBot:
    def __init__(self):
        self.config = Settings()
        self.logger = setup_logger()
        self.logger.info("Iniciando bot en modo LIVE + PayPal P2P...")

        self.paypal = PayPalP2P()
        self.bitso = BitsoTrader()
        
        if self.bitso.client is None:
            self.logger.error("No se pudo conectar a Bitso. Revisa bitso_keys.json")
            exit(1)

        self.trader = Trader()
        self.research = MarketResearch(self.bitso.client)

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.research_cycle, 'interval', minutes=2)
        self.scheduler.start()

        self.logger.info("Bot iniciado correctamente. Investigación cada 2 min.")

    def research_cycle(self):
        try:
            self.logger.info("Iniciando ciclo de investigación...")
            signals = self.research.scan_memecoins()
            for sig in signals:
                action = self.research.analyze_signal(sig['symbol'])
                if action == 'BUY':
                    self.trader.execute_trade(sig['symbol'], 'BUY')
            self.trader.check_positions()
        except Exception as e:
            self.logger.error(f"Error en ciclo: {e}")

    def start(self):
        self.logger.info("Bot en ejecución 24/7...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Bot detenido por el usuario.")
            self.scheduler.shutdown()