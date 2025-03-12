# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import logging
from utils.logger import logger
from config import BOT_TOKEN
from handlers import start, property_search, property_sell, excursion, callback_handlers

async def main() -> None:
    """
    Главная асинхронная функция для запуска основного бота.
    Инициализирует бота, регистрирует роутеры и начинает polling для обработки обновлений.
    """
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_routers(
        start.router,
        property_search.router,
        property_sell.router,
        excursion.router,
        callback_handlers.router
    )

    try:
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