import logging
from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.database import Session, User

# --- UTILIDADES ---

def generar_teclado_horas():
    # Rango de 09:00 a 23:00 + 00:00
    horas = [f"{h:02d}:00" for h in range(9, 24)]
    horas.append("00:00")
    
    keyboard = []
    for i in range(0, len(horas), 4):
        fila = [InlineKeyboardButton(hora, callback_data=f"hora_{hora}") for hora in horas[i:i+4]]
        keyboard.append(fila)
    
    return InlineKeyboardMarkup(keyboard)

def limpiar_todos_los_jobs(user_id, context):
    """Elimina cualquier rastro de vigilancia previa de forma segura."""
    if not context.job_queue:
        logging.error("¡ALERTA! El JobQueue no está disponible.")
        return

    for job_name in [f"fijo_{user_id}", f"morning_{user_id}"]:
        jobs = context.job_queue.get_jobs_by_name(job_name)
        if jobs:
            for j in jobs:
                j.schedule_removal()

# --- BOT LOGIC ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Vigilancia Fija 🔒", callback_data="set_modo_fijo")],
        [InlineKeyboardButton("Vigilancia Flexible 🔓", callback_data="set_modo_flexible")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👁️ **TELEPANTALLA ACTIVADA**\n\nCiudadano, el Gran Hermano requiere que elija su método de disciplina de lectura:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def manejar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    await query.answer()

    with Session() as session:
        # 1. Selección de Modo
        if data == "set_modo_fijo":
            context.user_data['temp_modo'] = 'fijo'
            await query.edit_message_text(
                "Has elegido **Modo Fijo**. Selecciona la hora de tu reeducación diaria:",
                reply_markup=generar_teclado_horas(),
                parse_mode='Markdown'
            )

        elif data == "set_modo_flexible":
            limpiar_todos_los_jobs(user_id, context)
            
            user = session.query(User).filter_by(user_id=user_id).first()
            if not user:
                user = User(user_id=user_id)
                session.add(user)
            
            user.modo = 'flexible'
            user.hora_fija = None
            session.commit()
            
            context.job_queue.run_daily(
                consulta_matutina, 
                time=time(8, 0), 
                chat_id=user_id,
                name=f"morning_{user_id}"
            )
            
            await query.edit_message_text(
                "**Modo Flexible activado.**\nLa Telepantalla te preguntará cada mañana. Selecciona tu hora para **HOY**:",
                reply_markup=generar_teclado_horas(),
                parse_mode='Markdown'
            )

        # 2. Selección de Hora (TODO este bloque debe estar indentado)
        elif data.startswith("hora_"):
            hora_elegida = data.split("_")[1]
            h, m = map(int, hora_elegida.split(':')) # Ahora esto solo corre si hay una hora
            
            user = session.query(User).filter_by(user_id=user_id).first()
            if not user:
                user = User(user_id=user_id)
                session.add(user)

            if context.user_data.get('temp_modo') == 'fijo':
                limpiar_todos_los_jobs(user_id, context)
                
                user.modo = 'fijo'
                user.hora_fija = hora_elegida
                session.commit()
                
                context.job_queue.run_daily(
                    alarma_lectura, 
                    time=time(h, m), 
                    chat_id=user_id, 
                    name=f"fijo_{user_id}"
                )
                
                await query.edit_message_text(f"✅ Disciplina fija establecida: {hora_elegida}. El Gran Hermano vigila.")
                context.user_data['temp_modo'] = None
            
            else:
                # Modo Flexible: Alarma de un solo uso para hoy
                context.job_queue.run_once(alarma_lectura, when=time(h, m), chat_id=user_id)
                await query.edit_message_text(f"✅ Horario para hoy registrado: {hora_elegida}. No falles al Partido.")
    

# --- FUNCIONES DE APOYO ---

async def alarma_lectura(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id, 
        text="📢 ¡ATENCIÓN! La lectura es fuerza. Inicia tu sesión ahora o serás reportado al Ministerio del Amor."
    )

async def consulta_matutina(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text="☀️ Ciudadano, el sol sale y el Gran Hermano espera su reporte. ¿A qué hora leerá hoy?",
        reply_markup=generar_teclado_horas()
    )