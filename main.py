from aiogram import Bot, Dispatcher, executor, types
import datetime
import requests
from aiogram.types import ContentType, Message, InputFile




API_TOKEN = '6083003984:AAHXRKN8zxyBlyLMjJkAgoD99RytkijFs7o'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
openweather_token = 'baf5502c93346631aa40f65e1b5e85b3'

#1
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply("Привет! (/help - список команд)\U0001F609")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
	await message.reply(
		f"Список команд, которые тебе помогут: \n\n"
		f"/start - начало работы с ботом\n\n"
		f"/help - список команд\n\n"
		f"/weather - погода в вашем городе\n\n"
		f"/schedule - расписание занятий на завтра\n\n"
		)










@dp.message_handler(commands=['weather2'])
async def weather_get(message: types.Message):
	try:
		await bot.send_message(message.from_user.id, "город")
		r = requests.get(
			f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={openweather_token}&units=metric"
			
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

	except:
		await message.reply("Проверьте название!")




#@dp.message_handler(content_types=ContentType.PHOTO)
#async def photo_send_id(message: Message):
	#await message.reply(message.photo[-1].file_id)


#@dp.message_handler(commands='photo')
##async def photo_send(message: Message):
	#chat_id = message.from_user.id
	#photo_file_id = 'AgACAgIAAxkBAAIBQmPwl2I8g8BQRKbL6vOwPoFRs0aZAALWwjEbbTuJS4Dx70DXZoUrAQADAgADeQADLgQ'


	#await dp.bot.photo_send(chat_id=chat_id, photo_send_id)




if __name__ == '__main__':
	executor.start_polling(dp)	