# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update
from aiogram.dispatcher.middlewares.base import BaseMiddleware
import json
import os
import logging
from utils.logger import logger
from config import BOT_TOKEN, bot_status, update_bot_status, STATUS_FILE

from handlers import start, property_search, property_sell, excursion, callback_handlers

class PauseMiddleware(BaseMiddleware):
    """
    Middleware для проверки статуса паузы бота перед обработкой каждого обновления.
    Если бот паузирован (is_active = false), игнорирует обновления.
    """
    async def __call__(self, handler, event: Update, data: dict) -> None:
        """
        Проверяет статус бота и решает, продолжить ли обработку обновления.

        Args:
            handler: Следующий обработчик в цепочке.
            event (Update): Обновление от Telegram.
            data (dict): Данные контекста для обработки.
        """
        with open(STATUS_FILE, "r") as f:
            status = json.load(f)
        if not status.get("is_active", True):
            user_id = event.message.from_user.id if event.message else "unknown"
            logger.info(f"Бот паузирован, обновление от {user_id} проигнорировано.")
            return  # Игнорируем обновление
        return await handler(event, data)

async def main() -> None:
    """
    Главная асинхронная функция для запуска основного бота.
    Инициализирует бота, регистрирует роутеры и начинает polling.
    """
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # Регистрация middleware для проверки паузы
    dp.update.middleware(PauseMiddleware())

    # Регистрация роутеров
    dp.include_routers(
        start.router,
        property_search.router,
        property_sell.router,
        excursion.router,
        callback_handlers.router
    )

    try:
        logger.info("Бот запущен.")
        await dp.start_polling(bot)
    finally:
        await dp.stop_polling()
        await bot.session.close()
        logger.info("Основной бот завершил работу.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Основной бот остановлен пользователем.")