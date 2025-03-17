# admin_bot/main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import ADMIN_BOT_TOKEN, ADMIN_IDS
from utils.database import db
from utils.logger import logger

from admin_bot.handlers import start, control, messaging

async def main() -> None:
    """
    Главная асинхронная функция для запуска админ-бота.
    Инициализирует бота, регистрирует роутеры и функцию startup,
    затем начинает polling для обработки обновлений.
    """
    bot = Bot(token=ADMIN_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # Инициализация базы данных
    await db.connect()

    # Регистрация роутеров
    dp.include_routers(
        start.router,
        control.router,
        messaging.router
    )

    async def on_startup(bot: Bot) -> None:
        """
        Функция, вызываемая при старте бота.
        Отправляет уведомление всем администраторам из ADMIN_IDS.

        Args:
            bot (Bot): Экземпляр бота для отправки сообщений.
        """
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(admin_id, "Админ-бот запущен. Используйте /start.")
            except Exception:
                logger.error(f"Не удалось отправить сообщение админу с ID {admin_id}")

    dp.startup.register(on_startup)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.stop_polling()
        await bot.session.close()
        await db.close()  # Закрываем базу данных
        logger.info("Админ-бот завершил работу.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Админ-бот остановлен пользователем.")