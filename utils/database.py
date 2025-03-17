# utils/database.py
from typing import List

import aiosqlite
import logging
from datetime import datetime  # Добавляем импорт datetime
from utils.logger import logger

class Database:
    """
    Класс для асинхронного взаимодействия с базой данных SQLite.
    Используется для хранения и управления списком пользователей.
    """
    def __init__(self, db_name: str = "users.db"):
        """
        Инициализация базы данных.

        Args:
            db_name (str): Имя файла базы данных.
        """
        self.db_name = db_name
        self.db = None

    async def connect(self) -> None:
        """
        Устанавливает соединение с базой данных и создает таблицу users, если она не существует.
        """
        self.db = await aiosqlite.connect(self.db_name)
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                timestamp TEXT NOT NULL
            )
        """)
        await self.db.commit()
        logger.info("Соединение с базой данных установлено.")

    async def close(self) -> None:
        """
        Закрывает соединение с базой данных.
        """
        if self.db:
            await self.db.close()
            logger.info("Соединение с базой данных закрыто.")

    async def register_user(self, user_id: int) -> bool:
        """
        Регистрирует нового пользователя в базе данных, если его еще нет.

        Args:
            user_id (int): ID пользователя Telegram.

        Returns:
            bool: True, если регистрация успешна или пользователь уже зарегистрирован, False в случае ошибки.
        """
        try:
            # Проверяем, существует ли пользователь
            cursor = await self.db.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            exists = await cursor.fetchone()

            if exists:
                logger.info(f"Пользователь {user_id} уже зарегистрирован в базе данных")
                return True

            # Регистрируем нового пользователя
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await self.db.execute(
                "INSERT INTO users (user_id, timestamp) VALUES (?, ?)",
                (user_id, timestamp)
            )
            await self.db.commit()
            logger.info(f"Пользователь {user_id} успешно зарегистрирован в базе данных")
            return True
        except Exception as e:
            logger.error(f"Ошибка регистрации пользователя {user_id}: {str(e)}")
            return False

    async def get_all_users(self) -> List[int]:
        """
        Получает список всех зарегистрированных пользователей.

        Returns:
            List[int]: Список ID пользователей.
        """
        try:
            cursor = await self.db.execute("SELECT user_id FROM users")
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            logger.error(f"Ошибка получения списка пользователей: {str(e)}")
            return []

# Глобальный экземпляр базы данных
db = Database()