from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
# from os import qetenv
from async_magnit import collect_data
from aiofiles import os

bot = Bot(token='')
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Moskow ', 'Ekataterinburg', 'Krasnodar']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Select a City', reply_markup=keyboard)


@dp.message_handler(Text(equals='Moskow'))
async def moskow_city(message: types.Message):
    await message.answer('Please waiting ...')
    chat_id = message.chat.id
    await send_data(city_code='2398', chat_id=chat_id)


@dp.message_handler(Text(equals='Ekataterinburg'))
async def ekb_city(message: types.Message):
    await message.answer('Please waiting ...')
    chat_id = message.chat.id
    await send_data(city_code='1869', chat_id=chat_id)


@dp.message_handler(Text(equals='Krasnodar'))
async def krd_city(message: types.Message):
    await message.answer('Please waiting ...')
    chat_id = message.chat.id
    await send_data(city_code='1761', chat_id=chat_id)


async def send_data(city_code='2398', chat_id=''):
    file = await collect_data(city_code=city_code)
    await bot.send_document(chat_id=chat_id, document=open(file, 'rb'))
    await os.remove(file)

if __name__ == '__main__':
    executor.start_polling(dp)