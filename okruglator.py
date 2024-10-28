__version__ = (1, 1, 4)

#            © Copyright 2024
#           https://t.me/HikkTutor 
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
# meta banner:https://t.me/HikkTutor
# name: okruglator
import subprocess
from telethon.tl.types import DocumentAttributeVideo
from telethon.errors import ChatAdminRequiredError
from .. import loader
import os
import asyncio
from collections import deque
import uuid

MAX_VIDEO_DURATION = 60 
MAX_VIDEO_SIZE_MB = 25 

@loader.tds
class okruglator(loader.Module):
    """Модуль для преобразования видео в видео-сообщение (кружок)."""

    strings = {"name": "okruglator"}
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "show_progress",
                True,
                lambda: "Отображать прогресс загрузки?",
                validator=loader.validators.Boolean()
            ),
        )
        self.active_tasks = 0
        self.task_queue = deque()
        self.last_message_text = ""

    async def client_ready(self, client, db):
        self.client = client

    async def display_progress(self, message, text, current=None, total=None):
        """Отображает прогресс выполнения."""
        if self.config["show_progress"] and current is not None and total is not None:
            percent = int(current / total * 100)
            filled_blocks = percent // 10
            new_text = f"<b>{text}</b> [{'■' * filled_blocks}{'□' * (10 - filled_blocks)}] {percent}%"
        else:
            new_text = f"<b>{text}...</b>"

        if new_text != self.last_message_text:
            await message.edit(new_text)
            self.last_message_text = new_text

    async def process_video(self, message, video, reply):
        """Обработка видео."""
        self.active_tasks += 1

        unique_id = uuid.uuid4()
        video_path = f"input_video_{unique_id}.mp4"
        output_path = f"output_video_{unique_id}.mp4"

        try:
            if self.active_tasks == 2:
                await message.edit("<b>Обработка 2 видео нагружает сервер сильнее</b>")
                await asyncio.sleep(0.9) 

            if self.active_tasks > 2:
                await message.edit("<b>Нельзя обрабатывать больше видео</b>")
                self.active_tasks -= 1 
                return

            if video.size > MAX_VIDEO_SIZE_MB * 1024 * 1024:
                await message.edit("<b>Видео превышает максимальный размер 25 МБ.</b>")
                self.active_tasks -= 1
                return

            if self.config["show_progress"]:
                await self.display_progress(message, "Скачиваю видео", 0, 1)
                await message.client.download_media(
                    video,
                    video_path,
                    progress_callback=lambda d, t: asyncio.ensure_future(
                        self.display_progress(message, "Скачиваю видео", d, t)
                    )
                )
            else:
                await message.edit("<b>Скачиваю видео...</b>")
                self.last_message_text = "<b>Скачиваю видео...</b>"
                await message.client.download_media(video, video_path)

            await message.edit("<b>Обрабатываю видео...</b>")
            self.last_message_text = "<b>Обрабатываю видео...</b>"
            ffmpeg_command = [
                'ffmpeg', '-i', video_path, '-vf', 'crop=min(iw\\,ih):min(iw\\,ih),scale=480:480,format=yuv420p',
                '-codec:v', 'libx264', '-preset', 'fast', '-tune', 'zerolatency', '-t', str(MAX_VIDEO_DURATION), '-y', output_path
            ]

            process = subprocess.run(ffmpeg_command, stderr=subprocess.PIPE, text=True)
            if process.returncode != 0:
                raise Exception(f"FFmpeg error: {process.stderr}")

            if self.config["show_progress"]:
                await self.display_progress(message, "Отправляю кружок", 0, 1)
                try:
                    await message.client.send_file(
                        message.to_id,
                        file=output_path,
                        attributes=[DocumentAttributeVideo(round_message=True, duration=0, w=480, h=480)],
                        reply_to=reply.id if reply else None,
                        progress_callback=lambda d, t: asyncio.ensure_future(
                            self.display_progress(message, "Отправляю видео-сообщение", d, t)
                        )
                    )
                except ChatAdminRequiredError:
                    await message.edit("<b>В этом чате запрещены кружки.</b>")
            else:
                await message.edit("<b>Отправляю видео-сообщение...</b>")
                self.last_message_text = "<b>Отправляю видео-сообщение...</b>"
                try:
                    await message.client.send_file(
                        message.to_id,
                        file=output_path,
                        attributes=[DocumentAttributeVideo(round_message=True, duration=0, w=480, h=480)],
                        reply_to=reply.id if reply else None
                    )
                except ChatAdminRequiredError:
                    await message.edit("<b>В этом чате запрещены кружки.</b>")

            await message.delete()
        except Exception as e:
            if self.active_tasks == 2:
                await message.edit("<b>Произошла ошибка при обработке второго видео. Вношу задачу в очередь для повторной обработки.</b>")
                self.task_queue.append((message, video, reply))
            else:
                await message.edit(f"<b>Ошибка: {str(e)}</b>")
        finally:
            self.active_tasks -= 1
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(output_path):
                os.remove(output_path)

            if self.task_queue and self.active_tasks < 2:
                next_task = self.task_queue.popleft()
                await self.process_video(*next_task)

    async def okrcmd(self, message):
        """Переделать (Видео, gif, sticker) в Кружок"""
        if self.active_tasks >= 2:
            await message.edit("<b>Слишком много запросов! Подождите, пока не завершится обработка других видео.</b>")
            return

        reply = await message.get_reply_message()
        video = reply.video if reply and reply.video else (message.video if message.video else None)

        if not video:
            await message.edit("<b>Ага, а видео где?</b>")
            return

        if any(isinstance(attr, DocumentAttributeVideo) and attr.round_message for attr in video.attributes):
            await message.edit("<b>Кружок из кружка? Круто ты это придумал(а)...</b>")
            return

        asyncio.create_task(self.process_video(message, video, reply))