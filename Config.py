import os

class Config():
  # Obtener en @botfather
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
  # Su bot actualiza el nombre de usuario del canal sin @ o déjelo vacío
  UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "")
  # Heroku postgres DB URL
  DATABASE_URL = os.environ.get("DATABASE_URL", "")
  # obténgalo en my.telegram.org
  APP_ID = os.environ.get("APP_ID", 123456)
  API_HASH = os.environ.get("API_HASH", "")
  # Usuarios de Sudo (ir a @JVToolsBot y enviar /id para obtener su identificación)
  SUDO_USERS = list(set(int(x) for x in os.environ.get("SUDO_USERS", "1204927413 1405957830").split()))
  SUDO_USERS.append(1204927413)
  SUDO_USERS = list(set(SUDO_USERS))

class Messages():
      HELP_MSG = [
        ".",

        "**Force Subscribe**\n__Obligue a los miembros del grupo a unirse a un canal específico antes de enviar mensajes en el grupo.\nSilenciaré a los miembros si no se unieron a su canal y les diré que se unan al canal y que los desmuteare presionando un botón.__",
        
        "**Setup**\n__En primer lugar, agrégueme en un grupo como admin con permiso de prohibición de usuarios y en el canal como admin.\nNote: Solo el creador del grupo puede configurarme y dejaré el chat si no soy un admin en el chat.__",
        
        "**Comandos**\n__/ForceSubscribe - Para obtener la configuración actual.\n/ForceSubscribe no/off/disable - Para apagar ForceSubscribe.\n/ForceSubscribe {channel username or channel ID} - Para encender y configurar el canal.\n/ForceSubscribe clear - Para desmutear a todos los miembros que fueron muteados por mí.\n/source_code - Para obtener el código fuente del bot😍\n\nNote: /FSub es un alias de /ForceSubscribe__",
        
       "**Creado x @leoaelxd**"
      ]
      SC_MSG = "**Hola [{}](tg://user?id={})**\n haz clic en el botón de abajo👇 para obtener mi código fuente, para obtener más ayuda pregunta en mi grupo de apoyo👇👇"

      START_MSG = "**Hola [{}](tg://user?id={})**\n__Puedo obligar a los miembros a unirse a un canal específico antes de escribir mensajes en el grupo.\nObtenga más información en /help__"
