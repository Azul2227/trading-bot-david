from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
import threading

class TradingBotApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.status = Label(text="Conectando...", size_hint_y=0.3, font_size=24)
        self.balance = Label(text="Saldo: -- USDT", size_hint_y=0.2)
        self.positions = Label(text="Posiciones: 0", size_hint_y=0.2)
        self.btn = Button(text="Actualizar", size_hint_y=0.2)
        self.btn.bind(on_press=self.update)

        layout.add_widget(self.status)
        layout.add_widget(self.balance)
        layout.add_widget(self.positions)
        layout.add_widget(self.btn)

        # Actualizar cada 10 seg
        threading.Timer(10, self.auto_update).start()

        return layout

    def update(self, *args):
        UrlRequest(
            "https://trading-bot-david.onrender.com/data",
            on_success=self.on_data,
            timeout=10
        )

    def auto_update(self):
        self.update()
        threading.Timer(10, self.auto_update).start()

    def on_data(self, req, result):
        self.status.text = "BOT ACTIVO 24/7"
        self.balance.text = f"Saldo: {result['balance']:.2f} USDT"
        self.positions.text = f"Posiciones: {result['positions']}"

TradingBotApp().run()