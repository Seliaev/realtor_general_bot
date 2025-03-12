# utils/notify_admin.py
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from config import ADMIN_BOT_TOKEN, ADMIN_IDS
import asyncio

bot = Bot(token=ADMIN_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

async def notify_admins(message_text: str) -> None:
    """
    Асинхронно отправляет уведомление всем администраторам, указанным в ADMIN_IDS.

    Args:
        message_text (str): Текст уведомления для отправки.
    """
    tasks = [bot.send_message(admin_id, message_text) for admin_id in ADMIN_IDS]
    await asyncio.gather(*tasks)