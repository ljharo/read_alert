# Telepantalla: Tu Asistente de Disciplina de Lectura (Gran Hermano)

¡Bienvenido a Telepantalla! Este es un bot de Telegram diseñado para ayudarte a mantener una disciplina de lectura constante, con un toque lúdico inspirado en el Gran Hermano. El bot te recordará tus hábitos de lectura, asegurándose de que "el Partido" esté contento con tu progreso.

## Características

*   **Modo de Vigilancia Fija:** Establece una hora específica cada día para recibir un recordatorio de lectura. ¡El Gran Hermano vigila tu compromiso!
*   **Modo de Vigilancia Flexible:** Recibe una consulta matutina para que elijas tu hora de lectura para ese día, adaptándose a tu agenda. ¡Pero no te olvides de leer!
*   **Personalización:** Elige el modo de vigilancia que mejor se adapte a tus necesidades.
*   **Persistencia de Datos:** Utiliza SQLite para almacenar tus preferencias de modo y hora, asegurando que el Gran Hermano nunca olvide tu compromiso.

## Cómo Funciona

El bot ofrece dos modos principales:

1.  **Vigilancia Fija:** Una vez que estableces una hora, el bot te enviará un mensaje recordatorio a esa misma hora todos los días.
2.  **Vigilancia Flexible:** Cada mañana, el bot te preguntará a qué hora planeas leer ese día, permitiéndote seleccionar una hora para una alarma de un solo uso.

## Configuración y Ejecución con Docker Compose

Para poner en marcha tu propia Telepantalla, sigue estos pasos:

### Prerrequisitos

*   Docker y Docker Compose instalados en tu sistema.

### 1. Obtén tu Token de Bot de Telegram

Habla con el [BotFather](https://t.me/BotFather) en Telegram para crear un nuevo bot y obtener tu `TELEGRAM_TOKEN`.

### 2. Configura las Variables de Entorno

Crea un archivo `.env` en la raíz de tu proyecto (al mismo nivel que `docker-compose.yml`) con las siguientes variables:

```
TELEGRAM_TOKEN=TU_TOKEN_DE_TELEGRAM
DATABASE_URL=sqlite:///big_brother.db
```
**Nota:** `DATABASE_URL` para SQLite es `sqlite:///big_brother.db`. Puedes cambiar `big_brother.db` por el nombre que prefieras para tu archivo de base de datos. Para bases de datos PostgreSQL o MySQL, el formato sería diferente.

### 3. Ejecuta el Bot

Navega hasta el directorio raíz de tu proyecto en la terminal y ejecuta:

```bash
docker-compose up --build -d
```

*   `docker-compose up`: Inicia los servicios definidos en `docker-compose.yml`.
*   `--build`: Construye la imagen Docker de tu bot (necesario la primera vez o después de cambios en el código/Dockerfile).
*   `-d`: Ejecuta los contenedores en segundo plano.

### 4. Interactúa con tu Bot

Abre Telegram, busca tu bot y envíale el comando `/start`. ¡El Gran Hermano te está esperando!

### Detener el Bot

Para detener el bot y los contenedores:

```bash
docker-compose down
```

## Desarrollo Local (sin Docker)

Si prefieres ejecutar el bot directamente en tu entorno Python:

### 1. Prerrequisitos

*   Python 3.9+ instalado.
*   Un entorno virtual (recomendado).

### 2. Configura el Entorno Virtual e Instala Dependencias

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configura las Variables de Entorno

Crea un archivo `.env` en la raíz de tu proyecto (al mismo nivel que `main.py`) con las variables `TELEGRAM_TOKEN` y `DATABASE_URL` como se explicó anteriormente.

### 4. Ejecuta el Bot

```bash
python main.py
```

## Estructura del Proyecto

*   `main.py`: Punto de entrada principal del bot de Telegram.
*   `app/`: Contiene la lógica principal del bot.
    *   `bot.py`: Lógica del bot, manejadores de comandos y callbacks.
    *   `constans.py`: Carga variables de entorno.
    *   `database.py`: Definición del modelo de usuario y configuración de la base de datos (SQLAlchemy).
*   `big_brother.db`: Archivo de base de datos SQLite (creado automáticamente).
*   `requirements.txt`: Dependencias del proyecto.
*   `Dockerfile`: Define cómo construir la imagen Docker del bot.
*   `docker-compose.yml`: Configuración para ejecutar el bot con Docker Compose.
*   `.dockerignore`: Archivos y directorios a ignorar por Docker.
