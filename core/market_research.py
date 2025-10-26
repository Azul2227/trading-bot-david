# core/market_research.py
# ESCANEA MEMECOINS CON ALTO VOLUMEN Y VOLATILIDAD

import logging

class MarketResearch:
    def __init__(self, bitso_client):
        self.client = bitso_client

    def scan_memecoins(self):
        symbols = ['doge_mxn', 'shib_mxn', 'pepe_mxn']
        high_volume = []
        for sym in symbols:
            try:
                t = self.client.ticker(book=sym)
                vol = float(t.volume)
                change = abs(float(t.high) - float(t.low)) / float(t.last)
                if vol > 500000 and change > 0.03:
                    high_volume.append({'symbol': sym, 'volume': vol, 'change': change})
            except: continue
        return sorted(high_volume, key=lambda x: x['change'], reverse=True)[:3]

    def analyze_signal(self, symbol):
        return 'BUY'  # Bot proactivo