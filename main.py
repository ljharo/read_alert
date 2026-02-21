import pytz
import logging
from datetime import time
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, Defaults
from app.bot import start, manejar_callback, alarma_lectura, consulta_matutina
from app.constans import TELEGRAM_TOKEN
from app.database import Session, User

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def post_init(application):
    """
    Esta función se ejecuta justo después de que el bot inicia.
    Aquí recuperamos la vigilancia de todos los ciudadanos.
    """
    print("Recuperando registros del Ministerio de la Verdad...")
    session = Session()
    usuarios = session.query(User).all()

    for user in usuarios:
        if user.modo == "fijo" and user.hora_fija:
            h, m = map(int, user.hora_fija.split(":"))
            # Programar la alarma diaria
            application.job_queue.run_daily(
                alarma_lectura,
                time=time(h, m),
                chat_id=user.user_id,
                name=f"fijo_{user.user_id}",
            )

        elif user.modo == "flexible":
            # Programar la pregunta matutina diaria
            application.job_queue.run_daily(
                consulta_matutina,
                time=time(8, 0),  # 8 AM por defecto
                chat_id=user.user_id,
                name=f"morning_{user.user_id}",
            )

    session.close()
    print("Vigilancia restablecida en todos los sectores.")


if __name__ == "__main__":
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN no detectado.")

    ZONA_HORARIA = pytz.timezone("America/Caracas")
    defaults = Defaults(tzinfo=ZONA_HORARIA)

    # Usamos post_init para cargar los datos de la DB al arrancar
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .defaults(defaults)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cambiar", start))
    app.add_handler(CallbackQueryHandler(manejar_callback))

    print("Telepantalla en línea... El Gran Hermano te observa.")
    app.run_polling()
