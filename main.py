from aiogram import Bot, Dispatcher, executor, types
import datetime
import requests, json
import modules.messages, modules.config, modules.accces
from modules.keyboard import defaultKeyboard

bot = Bot(modules.config.BOT_TOKEN)
dp = Dispatcher(bot)

admins = []

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply(modules.messages.START,
		     reply_markup=defaultKeyboard)
	admins = await modules.accces.getAdmins(bot, message)
	
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
	await message.reply(modules.messages.HELP,parse_mode='HTML')

@dp.message_handler(commands=['weather'])
async def weather_get(message: types.Message):
	r = requests.get(
		f"https://api.openweathermap.org/data/2.5/weather?q=rostov-on-don&appid={modules.config.OPENWEATHER_TOKEN}&units=metric"
		
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