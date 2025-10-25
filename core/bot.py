import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from core.trader import Trader
from core.market_research import MarketResearch
from utils.logger import setup_logger
from exchanges.bitso import BitsoTrader

class TradingBot:
    def __init__(self):
        self.bitso = BitsoTrader()
        self.logger = setup_logger()
        self.trader = Trader()
        self.research = MarketResearch(self.bitso.client)
        self.scheduler = BackgroundScheduler()
        self.running = True
        self.logger.info("Bot inicializado correctamente")

    def research_cycle(self):
        self.logger.info("Iniciando investigación de mercado...")
        signals = self.research.scan_memecoins()
        for sig in signals:
            action = self.research.analyze_signal(sig['symbol'])
            if action == 'BUY':
                self.trader.execute_trade(sig['symbol'], 'BUY')
            self.logger.info(f"Señal: {sig['symbol']} -> {action}")
            self.trader.notifier.send("¡BOT INICIADO! Telegram 100% activo")

    def start(self):
        # LIMPIAR JOBS ANTERIORES
        for job in self.scheduler.get_jobs():
            job.remove()

        # PROGRAMAR NUEVOS JOBS
        self.scheduler.add_job(self.research_cycle, 'interval', minutes=3, id='research_job')
        self.scheduler.add_job(self.trader.check_positions, 'interval', minutes=1, id='check_positions')

        try:
            self.scheduler.start()
            self.logger.info("Bot iniciado con APScheduler (MODO TESTNET)")

            # MANTENER VIVO
            while self.running:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.stop()
        except Exception as e:
            self.logger.error(f"Error en start(): {e}")
            self.stop()

    def stop(self):
        self.running = False
        try:
            if self.scheduler.running:
                self.scheduler.shutdown(wait=False)
            self.logger.info("Bot detenido correctamente")
        except:
            pass