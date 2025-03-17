# utils/google_sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEET_ID
import os
from typing import List, Any, Union
import logging
from utils.logger import logger
import sys
from datetime import datetime

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

class GoogleSheetsClient:
    """
    Класс для взаимодействия с Google Sheets через gspread.
    Позволяет добавлять строки, создавать листы и читать данные.
    """
    def __init__(self) -> None:
        """
        Инициализация клиента Google Sheets.
        Загружает учетные данные из credentials.json и открывает таблицу по GOOGLE_SHEET_ID.
        Если файл credentials.json отсутствует, выводит сообщение и завершает выполнение.
        """
        credentials_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials.json")
        if not os.path.exists(credentials_path):
            message = "Файл credentials.json не найден в корне проекта. Пожалуйста, добавьте его и перезапустите бота."
            logger.error(message)
            sys.exit(1)
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, SCOPES)
        self.client = gspread.authorize(self.credentials)
        self.spreadsheet = self.client.open_by_key(GOOGLE_SHEET_ID)

    def append_row(self, sheet_name: str, row_data: List[Any]) -> bool:
        """
        Добавление строки в указанный лист с временной меткой.
        Если лист не существует, он создается. Добавляет заголовки, если лист пуст.

        Args:
            sheet_name (str): Название листа (например, "SearchRequests").
            row_data (List[Any]): Данные для добавления в строку.

        Returns:
            bool: True, если строка успешно добавлена, False в случае ошибки.
        """
        try:
            try:
                worksheet = self.spreadsheet.worksheet(sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                self.create_sheet(sheet_name)
                worksheet = self.spreadsheet.worksheet(sheet_name)

            all_values = worksheet.get_all_values()
            if not all_values or (len(all_values) == 1 and not all_values[0]):
                if sheet_name == "SearchRequests":
                    headers = ["Property Type", "Rooms", "District", "Budget", "Condition", "Phone", "Telegram", "Timestamp"]
                else:
                    headers = ["Phone", "Telegram", "Timestamp"]
                worksheet.append_row(headers)

            # Добавляем временную метку в конец строки
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            row_data_with_timestamp = row_data + [timestamp]

            all_rows = worksheet.get_all_values()
            next_row = len(all_rows) + 1

            headers_count = len(worksheet.row_values(1)) if all_rows else 6
            if len(row_data_with_timestamp) < headers_count:
                row_data_with_timestamp.extend([""] * (headers_count - len(row_data_with_timestamp)))

            worksheet.update(f"A{next_row}", [row_data_with_timestamp])
            logger.info(f"Successfully appended row to {sheet_name} at row {next_row}: {row_data_with_timestamp}")
            return True
        except Exception as e:
            logger.info(f"Error appending row to {sheet_name}: {str(e)}")
            return False

    def create_sheet(self, sheet_name: str) -> None:
        """
        Создание нового листа, если он не существует.

        Args:
            sheet_name (str): Название создаваемого листа.
        """
        try:
            self.spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
            logger.info(f"Created new sheet: {sheet_name}")
        except gspread.exceptions.APIError as e:
            logger.info(f"Error creating sheet {sheet_name}: {str(e)}")

    def read_all_data(self, sheet_name: str) -> Union[List[List[str]], List]:
        """
        Чтение всех данных из указанного листа.

        Args:
            sheet_name (str): Название листа для чтения.

        Returns:
            Union[List[List[str]], List]: Список строк с данными из листа или пустой список в случае ошибки.
        """
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            return worksheet.get_all_values()
        except Exception as e:
            logger.info(f"Error reading data from {sheet_name}: {str(e)}")
            return []

gs_client = GoogleSheetsClient()

def append_row(sheet_name: str, row_data: List[Any]) -> bool:
    """
    Глобальная функция для добавления строки в указанный лист через экземпляр GoogleSheetsClient.

    Args:
        sheet_name (str): Название листа.
        row_data (List[Any]): Данные для добавления.

    Returns:
        bool: True, если строка добавлена, False в случае ошибки.
    """
    return gs_client.append_row(sheet_name, row_data)

def create_sheet(sheet_name: str) -> None:
    """
    Глобальная функция для создания нового листа через экземпляр GoogleSheetsClient.

    Args:
        sheet_name (str): Название создаваемого листа.
    """
    return gs_client.create_sheet(sheet_name)

def read_all_data(sheet_name: str) -> Union[List[List[str]], List]:
    """
    Глобальная функция для чтения всех данных из листа через экземпляр GoogleSheetsClient.

    Args:
        sheet_name (str): Название листа для чтения.

    Returns:
        Union[List[List[str]], List]: Список строк с данными или пустой список в случае ошибки.
    """
    return gs_client.read_all_data(sheet_name)