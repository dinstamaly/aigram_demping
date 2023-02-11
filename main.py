import asyncio
import json
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from report import get_report_file
from service import make_request

API_TOKEN = '5856952838:AAEfR4BOx8_2qNWh9jkMGxCKZxs7CFdu2f0'

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

dp.storage = MemoryStorage()

scheduled_chats = set()
inline_kb_full = InlineKeyboardMarkup(row_width=3)
inline_btn_3 = InlineKeyboardButton("Every Minute", callback_data='1')
inline_btn_4 = InlineKeyboardButton("Every 5 Minutes", callback_data='5')
inline_btn_5 = InlineKeyboardButton("Every 15 Minutes", callback_data='12')
inline_btn_6 = InlineKeyboardButton("Start", callback_data='start')
inline_btn_7 = InlineKeyboardButton("Stop", callback_data='stop')
inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5, inline_btn_6, inline_btn_7)


def make_json_file():
    s = make_request()
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        'Content-Type': 'application/json',
    }
    product_url = 'https://kaspi.kz/merchantcabinet/api/offer'
    request = s.post(
        product_url,
        headers=headers2,
        cookies=s.cookies.get_dict(),
        data=json.dumps({
            'offerStatus': "ACTIVE",
            'start': 0,
            'count': 200
        })

    )
    with open('my_product.json', 'w', encoding='utf-8') as my_json:
        json.dump(request.json(), my_json, ensure_ascii=False, indent=4)
    return request.json()


async def send_messages(interval: int, chat_id: int):
    print(interval)
    while chat_id in scheduled_chats:
        data = make_json_file()
        now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        await bot.send_message(chat_id=chat_id, text=f"Current time: {now}\nПодождите 5 мин, проводится операция")
        file = await get_report_file(data['offers'])
        with open('ExcelFormatTemplate.xlsx', 'wb') as f:
            f.write(file)
        await bot.send_document(chat_id=chat_id, document=open('ExcelFormatTemplate.xlsx', 'rb'))
        await asyncio.sleep(interval * 3600)


@dp.callback_query_handler(lambda c: c.data in ('1', '5', '15', 'stop'))
async def process_callback_schedule_time(callback_query: CallbackQuery):
    current_chat_id = callback_query.message.chat.id
    if callback_query.data == "stop":
        if current_chat_id in scheduled_chats:
            scheduled_chats.remove(current_chat_id)
        text = "Scheduling stopped."
    else:
        interval = int(callback_query.data)
        scheduled_chats.add(current_chat_id)
        asyncio.ensure_future(send_messages(interval, current_chat_id))
        text = f"Scheduling interval set to {interval} minutes."
    await bot.answer_callback_query(callback_query.id, text=text)


@dp.message_handler(commands='schedule')
async def cmd_schedule(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text='Choose a time interval:',
        reply_markup=inline_kb_full)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
