from aiogram import Bot, Dispatcher, executor, types
from pprint import pprint
import datetime
from config import openweather_token
import requests

API_TOKEN = '6083003984:AAHXRKN8zxyBlyLMjJkAgoD99RytkijFs7o'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
#1
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply("Привет бот, я бот ;)\nОтправь мне любое сообщение, я постараюсь ответить")

#3
@dp.message_handler()
async def weather_get(message: types.Message):
	try:
		r = requests.get(
			f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={openweather_token}&units=metric"
			)
		data = r.json()

		city = data["name"]
		temp_cur = data["main"]["temp"]
		humidity_cur = data["main"]["humidity"]
		wind_cur = data["wind"]["speed"]
		pressure_cur = data["main"]["pressure"]
		sunrise_cur = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
		sunset_cur = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
		sunr_minus_suns = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"]) 




		await message.reply(
			f"{datetime.datetime.now().strftime('%H-%M-(%d-%m-%Y)')}\n"
			f"Погода в городе: {city}\n"
			f"Температура: {temp_cur} °C\n"
			f"Влажность воздуха: {humidity_cur}%\n"
			f"Скорость ветра: {wind_cur} m/s\n"
			f"Атмосферное давление: {pressure_cur} мм.рт.ст\n"
			f"Восход: {sunrise_cur}\n"
			f"Заход: {sunset_cur}\n"
			f"Дневное время: {sunr_minus_suns}\n"
			f"Доброго дня!\n"
			)

	except:
		await message.reply("Проверьте название!")


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)