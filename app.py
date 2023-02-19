from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
import logging
import sqlite3


API_TOKEN = '6083003984:AAHXRKN8zxyBlyLMjJkAgoD99RytkijFs7o'
ADMINS = []
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
openweather_token = 'baf5502c93346631aa40f65e1b5e85b3'
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, block INTEGER);""")
conn.commit()


##Панель управления
kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(types.InlineKeyboardButton(text="Помощь"))
kb.add(types.InlineKeyboardButton(text="Администрация"))
kb.add(types.InlineKeyboardButton(text="Статистика"))




@dp.message_handler(commands=['admins'])
async def admins(message: Message):
  chat_admins = await bot.get_chat_administrators(message.chat.id)
  for admins in chat_admins:
      ADMINS.append(admins)


@dp.message_handler(commands=['start'])
async def start(message: Message):
  cur = conn.cursor()
  cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
  result = cur.fetchone()
  if message.from_user.id in ADMINS:
    await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=kb)



@dp.message_handler(content_types=['text'], text='Помощь')
async def send_help(message: types.Message, state: FSMContext):
  await message.answer(
    f"Список команд, которые тебе помогут: \n\n"
    )



@dp.message_handler(content_types=['text'], text='Администрация')
async def statis(message: types.Message, state: FSMContext):

  await message.answer(f'Кол-во админов: {len(ADMINS)}')

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)