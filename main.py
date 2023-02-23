from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
from aiogram.dispatcher import filters
import modules.messages, modules.config
from modules.keyboard import kb, kb1
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(modules.config.BOT_TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())
ADMINS = [1303880756]
class dialog(StatesGroup):
	otvet = State()



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply(modules.messages.START, reply_markup=kb)

@dp.message_handler(commands=['settings'])
async def send_settings(message: types.Message):

	await message.reply(modules.messages.SETTINGS, reply_markup=kb1)

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
	await message.reply(modules.messages.HELP,parse_mode='HTML', reply_markup=kb)

@dp.message_handler(commands=['back'])
async def back(message: types.Message):
	await message.reply(f'Возвращаемся...', reply_markup=kb)





@dp.message_handler(commands=['inpWeather'], state=None)
async def city(message: types.Message, state: FSMContext):
	await bot.send_message(message.chat.id, text='Введи город: ')
	await dialog.otvet.set()

@dp.message_handler(state=dialog.otvet)
async def namee(message: types.Message, state: FSMContext):
	global name 
	name = message.text
	await dialog.next()
	await message.reply(f'Твой город: {name}', reply_markup=kb1)	
	
	return name

@dp.message_handler(commands=['weather'])
async def weather_get(message: types.Message):
	r = requests.get(
		f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={modules.config.OPENWEATHER_TOKEN}&units=metric"
		
		)
	data = r.json()

	temp_cur = data["main"]["temp"]
	humidity_cur = data["main"]["humidity"]
	wind_cur = data["wind"]["speed"]
	pressure_cur = data["main"]["pressure"]
	sunrise_cur = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
	sunset_cur = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
	sunr_minus_suns = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"]) 

	
	await message.reply(
		f"***{datetime.datetime.now().strftime('%d.%m.%Y - %H:%M')}***\n"
		f"Температура: {temp_cur} °C\n"
		f"Влажность воздуха: {humidity_cur}%\n"
		f"Скорость ветра: {wind_cur} m/s\n"
		f"Атмосферное давление: {pressure_cur} мм.рт.ст\n"
		f"Восход: {sunrise_cur}\n"
		f"Заход: {sunset_cur}\n"
		f"Дневное время: {sunr_minus_suns}\n"
		f"Хорошего дня!\n"
		)



if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)	