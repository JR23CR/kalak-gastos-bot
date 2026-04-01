import os
import telebot
import requests

# --- CONFIGURACIÓN ---
# Estos valores los configuraremos en el Hosting (Render/Railway)
TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyEUjXXR7QiTWpbAc1tBl4gjX633854yX-wclQygI5o9hQNdt24yCDSn7LOFeMMinuv/exec"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def enviar_bienvenida(message):
    bot.reply_to(message, "💰 ¡Listo, Jose! Registra tus movimientos:\n/gasto 50 Gasolina\n/ingreso 1000 Pago cliente")

@bot.message_handler(commands=['gasto', 'ingreso'])
def registrar(message):
    try:
        # Separar el comando del resto del texto
        partes = message.text.split(maxsplit=2)
        if len(partes) < 2:
            return bot.reply_to(message, "❌ Formato incorrecto. Usa: /gasto [monto] [detalle]")

        tipo = "SALIDA" if "gasto" in partes[0] else "ENTRADA"
        monto = float(partes[1])
        descripcion = partes[2] if len(partes) > 2 else "Sin detalle"

        # Datos para enviar a Google Apps Script
        payload = {
            "tipo": tipo,
            "monto": monto,
            "descripcion": descripcion
        }

        # Enviamos la petición POST
        respuesta = requests.post(WEBHOOK_URL, json=payload)

        if respuesta.status_code == 200:
            bot.reply_to(message, f"✅ Registrado en Sheets:\n💰 Q{monto:.2f}\n📝 {descripcion}")
        else:
            bot.reply_to(message, "⚠️ El bot envió el dato pero Sheets no respondió correctamente.")

    except ValueError:
        bot.reply_to(message, "❌ El monto debe ser un número.")
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "❌ Ocurrió un error al conectar con Google Sheets.")

if __name__ == "__main__":
    print("Bot Kalak Gastos está corriendo...")
    bot.polling()
