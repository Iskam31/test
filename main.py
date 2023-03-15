from aiogram import Bot, Dispatcher, executor, types
import datetime
import requests
import modules.messages, modules.config, modules.accces
from modules.keyboard import defaultKeyboard

"""
test
"""
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

"""
/test
"""


bot = Bot(modules.config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

admins = []

"""
test
"""
class GetCity(StatesGroup):
    set_city_name = State()
    get_city_name = State()
    edit_city_name = State()
    
    
@dp.message_handler(commands=['setCity'])
async def setCity(message: types.Message, state: FSMContext):
	await message.answer('Введи город, чудила')
	await state.set_state(GetCity.set_city_name.state)

@dp.message_handler(state=GetCity.set_city_name)
async def getCity(message: types.Message, state: FSMContext):
	await state.update_data(city=message.text.lower())
	await state.set_state(GetCity.get_city_name.state)
	await message.answer('Введи /weather и получай свою погоду, урод')

@dp.message_handler(state=GetCity.get_city_name, commands=['editCity'])
async def editCity(message: types.Message, state: FSMContext):
	await message.answer('На какую погоду меняем ?')
	await state.set_state(GetCity.set_city_name.state)

@dp.message_handler(commands=['weather'], state=GetCity.get_city_name)
async def getWeather (message: types.Message, state: FSMContext):
	city = await state.get_data()
	query = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city['city']}&appid={modules.config.OPENWEATHER_TOKEN}&units=metric")
	data = query.json()
	temp_cur = data["main"]["temp"]
	name = data['name']
	await message.reply(
		f'Погода в городе {name} \n' +
   		f'Сейчас температура, {temp_cur} по цельсию \n' +
		'Всё, тебе хватит'
	)

"""
/test
"""

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply(modules.messages.START,
		     reply_markup=defaultKeyboard)
	admins = await modules.accces.getAdmins(bot, message)
	
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
	await message.reply(modules.messages.HELP,parse_mode='HTML')
"""""""""
@dp.message_handler(commands=['weather'])
async def weather_get(message: types.Message):
	r = requests.get(
		f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={modules.config.OPENWEATHER_TOKEN}&units=metric"
		
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
"""""""""

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)	
	dp.register_message_handler(getCity, state=GetCity.get_city_name)
	dp.register_message_handler(getWeather, commands='weather', state=GetCity.get_city_name)