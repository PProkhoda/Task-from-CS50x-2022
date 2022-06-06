from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
# from os import qetenv
from async_run import create_event new_runner 
from aiofiles import os

bot = Bot(token='')
dp = Dispatcher(bot)

name_run = ''
date_run = ''
name_creator = ''
distance = ''
time_run = ''
event_id = ''
user_id = ''



@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Event list ', 'New event', 'Add runner', 'Dell runner', 'List of event runners']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    user_id = message.from_user.id

    await message.answer('Select an action', reply_markup=keyboard)


@dp.message_handler(Text(equals='Event list'))
async def event_list(message: types.Message):
    await message.answer('Please enter name of run...')
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)