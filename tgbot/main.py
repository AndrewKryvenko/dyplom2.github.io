import asyncio
import json

from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, WebAppInfo


bot = Bot(token="6442089419:AAG4q9RlLlpJ7w4HEKusOqTXUA18MSMaK_w")
dp = Dispatcher()

@dp.message_handler(Command('start'))
async def start(message: types.Message, state: FSMContext):
    item1 = KeyboardButton(text="Вибрати товар", web_app=WebAppInfo(url='https://dyplom2.github.io/'))
    keyboard = ReplyKeyboardMarkup(keyboard=[[item1]], resize_keyboard=True)
    await bot.send_message(message.from_user.id,"ТУТ ПОЧАТКОВИЙ ТЕКСТ ПРИ КОМАНДІ СТАРТ", reply_markup=keyboard, parse_mode="Markdown")

@dp.message()
async def web_app(callback_query):
    json_data = callback_query.web_app_data.data
    parsed_data = json.loads(json_data)
    message = ""
    for i, item in enumerate(parsed_data['items'], start=1):
        position = int(item['id'].replace('item', ''))
        message += f"Позиція {position}\n"
        message += f"Вартість {item['price']}\n\n"

    message += f"Загальна вартість: {parsed_data['totalPrice']}"

    await bot.send_message(callback_query.from_user.id, f"""
    {message}
    """)
    await bot.send_message('', f"""
Нове замовлення
{message}
""")



async def main():
    from handlers import dp
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == "__main__":
        asyncio.run(main())