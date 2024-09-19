#            © Copyright 2024
#           https://t.me/HikkTutor 
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# name: bio farm 

from .. import loader, utils
from telethon import types, events # type: ignore
import asyncio
from telethon.errors.rpcerrorlist import YouBlockedUserError # type: ignore
import traceback

spam = None

@loader.tds
class stickersMod(loader.Module):
    """Этот модуль позволит копить био опыт/ресурсы
    
    (на балансе необходимо иметь био ресурсы)"""
    strings = {'name': 'bio farm'}
    
    async def stopzarcmd(self, message):
        """остановить фарм"""
        global spam
        spam = False
        await message.delete()
        
    async def zarcmd(self, message):
        """(@id/@user/t.me) заражение по айди"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Вы не указали айди или юзернейм</b> <emoji document_id=5406917170540068843>❗️</emoji>")
            return
        async with message.client.conversation(5443619563) as conv:
            try:
                await message.client.send_message(5443619563, f"Заразить {str(args)}")
                evt = await conv.wait_event(events.NewMessage(incoming=True, from_users=5443619563))
                await message.edit(str(evt.message.message))
            except Exception as e:
                error_trace = traceback.format_exc()
                error_msg = f"<b>Произошла ошибка в строке {e.__traceback__.tb_lineno}: {str(e)}</b>"
                await message.edit(error_msg)
                return
        
    async def masszarcmd(self, message):
        """(количество) запуск фарма"""
        chat = 5443619563
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Вы не указали количество</b> <emoji document_id=5406917170540068843>❗️</emoji>")
            return
        async with message.client.conversation(chat) as conv:
            try:
                await message.edit('<b>Фарм запущен...</b> <emoji document_id=5406873473542797476>⚗️</emoji>')
                global spam
                spam = True
                for i in range(0, int(args) + 1):
                    if spam == False:
                        break
                    await message.client.send_message(chat, "заразить сильного")
                    await asyncio.sleep(3)
                    await message.client.send_message(chat, "!купить вакцину")
                    await asyncio.sleep(3)
                spam = False
            except YouBlockedUserError:
                await message.edit("<b>Ирис заблокирован</b>")
                return
            except Exception as e:
                error_trace = traceback.format_exc()
                error_msg = f"<b>Произошла ошибка в строке {e.__traceback__.tb_lineno}: {str(e)}</b>"
                await message.edit(error_msg)
                return