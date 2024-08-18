from .. import loader, utils
from telethon import types, events
import asyncio
from telethon.errors.rpcerrorlist import YouBlockedUserError

spam = None

@loader.tds
class stickersMod(loader.Module):
  """by @Vsakoe0 | этот модуль позволит копить био опыт/ресурсы
  
  (на балансе необходимо иметь био ресурсы)"""
  strings = {'name':'bio farm'}
  
  async def stopzarcmd(self, message):
      """**остановить фарм**"""
      global spam
      spam = False
      await message.delete()
      
  async def zarcmd(self, message):
      """(**@id/@user/t.me**) заражение по айди""" 
      args = utils.get_args_raw(msg)
      if not args:
	      await msg.edit("Вы не указали айди или юзернейм")
	      return
      async with msg.client.conversation(5443619563) as conv:
          try:
              await msg.client.send_message(5443619563, f"Заразить {str(args)}")
              evt = await conv.wait_event(events.NewMessage(incoming=True, from_users=5443619563))
              await msg.edit(str(evt.message.message))
              
          except Exception as e:
              await msg.edit("Ирис заблокирован или произошла ошибка")
              return
      
  async def masszarcmd(self, message):
      """(количисво) **запуск фарма**"""
      chat = 5443619563
      args = utils.get_args_raw(message)
      if not args:
	        await message.edit("Вы не указали количество")
	        return
      async with message.client.conversation(chat) as conv:
          try:
              await message.edit('Фарм запущен')
              global spam
              spam = True
              for i in range(0, int(args)+1):
                if spam == False:
                    break
                await message.client.send_message(chat, "заразить сильного")
                await asyncio.sleep(3)
                await message.client.send_message(chat, "!купить вакцину")
                await asyncio.sleep(3)
              spam = False
          except YouBlockedUserError:
              await message.edit("Ирис заблокирован")
              return
