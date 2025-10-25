# core/market_research.py
import logging
from binance.client import Client

class MarketResearch:
    def __init__(self, binance_client: Client):
        self.client = binance_client

    def scan_memecoins(self):
        try:
            # Obtener todos los pares USDT
            info = self.client.get_exchange_info()
            usdt_pairs = [s['symbol'] for s in info['symbols'] if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING']
            
            high_volume = []
            for symbol in usdt_pairs:
                try:
                    ticker = self.client.get_24hr_ticker(symbol=symbol)
                    vol = float(ticker['quoteVolume'])
                    change = float(ticker['priceChangePercent'])
                    if vol > 1_000_000 and change > 3:
                        high_volume.append({
                            'symbol': symbol,
                            'volume': vol,
                            'change': change
                        })
                except:
                    continue
            
            # Ordenar por cambio y tomar top 3
            return sorted(high_volume, key=lambda x: x['change'], reverse=True)[:3]
            
        except Exception as e:
            logging.error(f"Error escaneando: {e}")
            return []

    def analyze_signal(self, symbol):
        # Análisis simple: siempre BUY si pasa filtro
        return 'BUY'