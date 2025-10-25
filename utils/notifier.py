import requests
import logging
import json
import smtplib
from email.mime.text import MIMEText

class TelegramNotifier:
    def __init__(self, token):
        self.token = token
        self.chat_id = None

    def send(self, message):
        if not self.chat_id:
            try:
                res = requests.get(f"https://api.telegram.org/bot{self.token}/getUpdates").json()
                if res['ok'] and res['result']:
                    self.chat_id = res['result'][0]['message']['chat']['id']
            except:
                pass
        if self.chat_id:
            requests.post(f"https://api.telegram.org/bot{self.token}/sendMessage", 
                         data={'chat_id': self.chat_id, 'text': message})

class EmailNotifier:
    def __init__(self):
        try:
            with open('config/gmail.json') as f:
                g = json.load(f)
            self.email = g['email']
            self.app_password = g['app_password']
        except FileNotFoundError:
            logging.error("config/gmail.json no encontrado")
        except json.JSONDecodeError:
            logging.error("config/gmail.json tiene formato inválido")
        except Exception as e:
            logging.error(f"Error configurando Email: {e}")

    def send(self, subject, body):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = self.email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email, self.app_password)
                server.send_message(msg)
        except Exception as e:
            logging.error(f"Error enviando email: {e}")