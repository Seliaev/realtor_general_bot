# utils/logger.py
import logging

# Настройка логгера
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),  # Логи записываются в файл bot.log
        logging.StreamHandler()          # Логи выводятся в консоль
    ]
)

logger = logging.getLogger('realtor_bot')