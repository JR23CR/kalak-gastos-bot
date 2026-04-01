import os
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- CONFIGURACIÓN POR VARIABLES DE ENTORNO ---
# En el hosting (Render/Railway) configuraremos estas llaves
TOKEN = os.getenv('TELEGRAM_TOKEN') 
SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME')
JSON_FILE = 'credenciales.json'

bot = telebot.TeleBot(TOKEN)

def conectar_hoja():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

@bot.message_handler(commands=['start'])
def enviar_bienvenida(message):
    bot.reply_to(message, "💰 ¡Hola Jose! Registra tus movimientos:\n/gasto 50 Almuerzo\n/ingreso 1000 Pago cliente")

@bot.message_handler(commands=['gasto', 'ingreso'])
def registrar(message):
    try:
        partes = message.text.split(maxsplit=2)
        tipo = "SALIDA" if "gasto" in partes[0] else "ENTRADA"
        monto = float(partes[1])
        descripcion = partes[2] if len(partes) > 2 else "Sin detalle"
        fecha = datetime.now().strftime('%d/%m/%Y %H:%M')

        # Guardar en Google Sheets
        hoja = conectar_hoja()
        hoja.append_row([fecha, tipo, monto, descripcion])

        bot.reply_to(message, f"✅ Registrado en Sheets:\nQ{monto:.2f} - {descripcion}")
    except Exception as e:
        bot.reply_to(message, "❌ Error. Usa: /gasto [monto] [detalle]")

if __name__ == "__main__":
    print("Bot Kalak Gastos activo...")
    bot.polling()
