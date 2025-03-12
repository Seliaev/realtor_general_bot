#handlers/start.py
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from keyboards.main_menu import get_main_menu
from utils.text_manager import get_text

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    photo = FSInputFile("pic/7694cf01-b877-4a89-be7a-3c1c3db2ff13.jpg")  # Указываем путь к файлу
    await message.answer_photo(
        photo=photo,
        caption=get_text("welcome", "greeting"),
        reply_markup=get_main_menu()
    )