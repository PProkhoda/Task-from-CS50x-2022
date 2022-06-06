import datetime
from fake_useragent import UserAgent
import csv
from gc import get_referents
from random import random
import requests
import aiohttp
import aiofiles
import asyncio
from aiocsv import AsyncWriter
import os
from cs50 import SQL
import sqlite3

# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.dispatcher.filters import Text
# # from os import qetenv
# from async_magnit import collect_data
# from aiofiles import os

# bot = Bot(token='')
# dp = Dispatcher(bot)


# @dp.message_handler(commands='start')
# async def start(message: types.Message):
#     start_buttons = ['Event list ', 'New event', 'Add runner', 'Dell runner', 'List of event runners']
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*start_buttons)

#     await message.answer('Select an action', reply_markup=keyboard)


# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///run.db")

__connetction = None


def get_connection():
    global __connetction
    if __connetction is None:
        __connetction = sqlite3.connect('run.db')
    return __connetction

# Create new event: 
def create_event(creator_name: str, run_name: str, date_run: str, distance: float, time_run: str):
# add creator_name = user_id = message.from_user.id
# add input event name
# add input date_run
# add input distance
# add input time of run
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO events (creator_name, run_name, date_run, distance, time_run) VALUES(?, ?, ?, ?, ?)",
                   (creator_name, run_name, date_run, distance, time_run))
    conn.commit()

# create new runner
def new_runner(event_id: int, name: str, notes: str):
# add name = user_id = message.from_user.id
    conn = get_connection()
    c = conn.cursor()
    # event_id = c.execute('SELECT id FROM events WHERE run_name = "?"', event_name)
    # print(event_id)
    c.execute('INSERT INTO peoples (name, notes, event_id) VALUES (?, ?, ?)', (name, notes, event_id))
    conn.commit()
    

# delete runner
# def dell_runner():
# dell name = user_id = message.from_user.id


# show list of events
def show_events():
# show list of events
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    # ua = UserAgent()

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM events')
    list = c.fetchall()
 
    with open(f'забег_{cur_time}.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                'ID Забега',
                'Имя создателя',
                'Дата/Время забега',
                'Дистанция',
                'Приблизительное время пробежки',
                'Название забега'
            ]
        )
        writer.writerows(
            list
        )    


# show runner list for events
# def show_runners():
# show runner list for events


if __name__ == '__main__':
    create_event(creator_name='Igor', run_name='deth1', date_run='10.06.2022 06:30', distance='10,8', time_run='1,05 hour')
    new_runner(event_id=1, name='runner Igor', notes='+1 runner')
    show_events()