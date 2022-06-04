import asyncio, requests, config

from aiogram import Bot,Dispatcher,types,executor
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from apscheduler.schedulers.background import BackgroundScheduler

from markup import keyboard_main
from DB import Database
from parser import parsing, pars
from modify import *

#GLOBALS
bot = Bot(token=config.TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
db = Database("database.db")

class State(StatesGroup):
    get_url = State()
    get_name = State()

@dp.message_handler(commands = ['start'],state=None)
async def start(message: types.Message):
    await message.answer(f'Привет, создаю нового пользователя\nid = {message.from_user.id}\nusername = {message.from_user.username}',reply_markup=keyboard_main)
    await message.answer(db.create_user(message.from_user.id))

# def parsing():
#     response = requests.get(url = 'https://yobit.net/api/3/ticker/btc_usd')
#     data = response.json()
#     btc_price = f"BTC: {round(data.get('btc_usd').get('last'),2)}$"
#     return (btc_price)

# async def main(id):
#     while True:
#         if State.while_state:
#             await asyncio.sleep(1)
#             await bot.send_message(id,parsing())
#         else:
#             return 0

@dp.message_handler(state=State.get_url)
async def get_url(message: types.Message,state: FSMContext):
    db.update_url(message.from_user.id,create_url(message.text))
    await message.answer("Отправьте ключевые слова, которые должны содержаться в названии товара")
    await State.get_name.set()

@dp.message_handler(state=State.get_name)
async def get_name(message: types.Message,state: FSMContext):
    db.update_key_word(message.from_user.id,message.text)
    await state.finish()

    loop = asyncio.get_event_loop()
    loop.create_task(pars(message.from_user.id,db,bot,db.get_url(message.from_user.id),db.get_query(message.from_user.id)))
    await message.answer("Слежение за вашим товаром начнется через минуту")


@dp.message_handler(Text(equals='Начать слежение'))
async def answer(message: types.Message, state: FSMContext):
    await message.answer('Отправьте мне URL avito за которым будем следить', reply_markup=keyboard_main)
    await State.get_url.set()
    # State.while_state = True
    # loop = asyncio.get_event_loop()
    # loop.create_task(main(message.from_user.id))

@dp.message_handler(Text(equals='Отключить слежение'))
async def answer(message: types.Message, state: FSMContext):
    await message.answer('Выключаю. Вы сможете перезапустить слежение через 1 минуту.', reply_markup=keyboard_main)
    db.deactivate_track(message.from_user.id)

if __name__ == '__main__':
    executor.start_polling(dp)




