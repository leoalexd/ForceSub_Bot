import time
import logging
from Config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
async def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = await client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (await client.get_me()).id:
          try:
            await client.get_chat_member(channel, user_id)
            await client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              await cb.message.delete()
          except UserNotParticipant:
            await client.answer_callback_query(cb.id, text="❗ Únete al 'Canal' y presione el botón 'Desmuteame' 😁", show_alert=True)
      else:
        await client.answer_callback_query(cb.id, text="❗ Estás muteado por los admins por otras razones🤫", show_alert=True)
    else:
      if not (await client.get_chat_member(chat_id, (await client.get_me()).id)).status == 'administrator':
        await client.send_message(chat_id, f"❗ **{cb.from_user.mention} está tratando de desmutear, pero no puedo hacerlo porque no soy un admin en este chat, agrégueme como administrador nuevamente.**\n__*C va epicamente del chat*...__")
        await client.leave_chat(chat_id)
      else:
        await client.answer_callback_query(cb.id, text="❗ Advertencia: No hagas clic en el botón si puedes escribir libremente..", show_alert=True)



@Client.on_message((filters.text | filters.media) & ~filters.private & ~filters.edited, group=1)
async def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not (await client.get_chat_member(chat_id, user_id)).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      if channel.startswith("-"):
          channel_url = await client.export_chat_invite_link(int(channel))
      else:
          channel_url = f"https://t.me/{channel}"
      try:
        await client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = await message.reply_text(
              " Hola {} Espero que tengas un buen dia 😊, pero no estas en el Canal. Unete usando el botón Entrar al Canal y luego presione el botón Desmuteame para que puedas escribir 😉".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
             reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Entrar al Canal", url=channel_url)
                ],
                [
                    InlineKeyboardButton("Desmuteame", callback_data="onUnMuteRequest")
                ]
            ]
        )
          )
          await client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          await sent_message.edit("❗ **No soy admin :c**\n__Hazme admin con permiso de prohibir usuario y agrégueme de nuevo.\n*C va epicamente del chat*...__")
          await client.leave_chat(chat_id)
      except ChatAdminRequired:
        await client.send_message(chat_id, text=f"❗ **No soy admin en el [Canal]({channel_url})**\n__Hazme admin en el canal y agrégame de nuevo.\n*C va epicamente del chat...__")
        await client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
async def config(client, message):
  user = await client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status == "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        await message.reply_text("❌ **Force Subscribe esta desabilitado correctamente.**")
      elif input_str.lower() in ('clear'):
        sent_message = await message.reply_text('**Desmuteando a todos los miembros muteados por mi 🥺**')
        try:
          for chat_member in (await client.get_chat_members(message.chat.id, filter="restricted")):
            if chat_member.restricted_by.id == (await client.get_me()).id:
                await client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          await sent_message.edit('✅ **Los miembros ya estan desmuteados UwU 😊**')
        except ChatAdminRequired:
          await sent_message.edit('❗ **No soy admin :c..**\n__No puedo desmutear a los miembros porque no soy admin en este chat, hazme admin con permiso de usuario de prohibición😡 __')
      else:
        try:
          await client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          if input_str.startswith("-"):
              channel_url = await client.export_chat_invite_link(int(input_str))
          else:
              channel_url = f"https://t.me/{input_str}"
          await message.reply_text(f"✅ **Force Subscribe esta activado**\n__Force Subscribe esta activado, todos los miembros del grupo tienen que entrar a este [Canal]({channel_url}) para enviar mensajes en este grupo.__", disable_web_page_preview=True)
        except UserNotParticipant:
          await message.reply_text(f"❗ **No es un admin en el canal**\n__Yo no soy admin en el [Canal]({channel_url}). Agrégame como admin para habilitar el ForceSubscribe.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          await message.reply_text(f"❗ **Invalido Canal Username/ID.**")
        except Exception as err:
          await message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        my_channel = sql.fs_settings(chat_id).channel
        if my_channel.startswith("-"):
            channel_url = await client.export_chat_invite_link(int(input_str))
        else:
            channel_url = f"https://t.me/{my_channel}"
        await message.reply_text(f"✅ **Force Subscribe esta habilitado en este canal.**\n__Para el [Canal]({channel_url})__", disable_web_page_preview=True)
      else:
        await message.reply_text("❌ **Force Subscribe esta desactivado en el chat.**")
  else:
      await message.reply_text("❗ **Creador del grupo requerido**\n__Tienes que ser creador del grupo para hacer eso ☹️ __")
