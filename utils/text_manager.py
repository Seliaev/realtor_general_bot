# utils/text_manager.py
import os
import yaml
from typing import Dict, Any
import logging
from utils.logger import logger

class TextManager:
    """
    Класс для управления текстовыми данными, загружаемыми из YAML-файлов.
    Позволяет получать тексты по категории и ключу.
    """
    def __init__(self) -> None:
        """
        Инициализирует объект TextManager и загружает тексты из YAML-файлов.
        """
        self.texts: Dict[str, Dict[str, Any]] = {}
        self.load_texts()

    def load_texts(self) -> None:
        """
        Загружает тексты из YAML-файлов в директории texts/.
        Поддерживаемые файлы: main_menu.yaml, responses.yaml, welcome.yaml, admin_menu.yaml.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        texts_dir = os.path.join(base_dir, "texts")

        for filename in ["main_menu.yaml", "responses.yaml", "welcome.yaml", "admin_menu.yaml"]:
            file_path = os.path.join(texts_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    category = os.path.splitext(filename)[0]
                    self.texts[category] = yaml.safe_load(f) or {}
            else:
                logger.info(f"Файл {file_path} не найден")

    def get_text(self, category: str, key: str) -> str:
        """
        Получает текст по категории и ключу из загруженных данных.

        Args:
            category (str): Категория текста (например, "main_menu").
            key (str): Ключ текста (например, "search_property").

        Returns:
            str: Текст, соответствующий категории и ключу, или "Текст не найден", если ключ отсутствует.
        """
        return self.texts.get(category, {}).get(key, "Текст не найден")

text_manager = TextManager()

def get_text(category: str, key: str) -> str:
    """
    Глобальная функция для получения текста по категории и ключу.
    Использует экземпляр TextManager для доступа к текстам.

    Args:
        category (str): Категория текста (например, "main_menu").
        key (str): Ключ текста (например, "search_property").

    Returns:
        str: Текст, соответствующий категории и ключу, или "Текст не найден", если ключ отсутствует.
    """
    return text_manager.get_text(category, key)