from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from app.bot import start, manejar_callback
from app.constans import TELEGRAM_TOKEN



if __name__ == '__main__':
    TOKEN = TELEGRAM_TOKEN
    
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN is not set in the environment variables.")
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # El comando /cambiar simplemente vuelve a llamar a start para elegir modo
    app.add_handler(CommandHandler("cambiar", start)) 
    app.add_handler(CallbackQueryHandler(manejar_callback))
    
    print("Telepantalla en línea...")
    app.run_polling()