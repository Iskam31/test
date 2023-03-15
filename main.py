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
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#Описание бота, диспетчера, состояний(для связи с пользователями)
bot = Bot(modules.config.BOT_TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())
AD = None
class dialog(StatesGroup):
	otvet = State()
	otvet_par = State()

#######################Запуск бота в телеграмм, посредством команды
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply(modules.messages.START, reply_markup=kb)

####################Команда настройки(выбор параметров погоды и города)
@dp.message_handler(commands=['settings'])
async def send_settings(message: types.Message):
	inbuttons = [types.InlineKeyboardButton(text = "Выбрать погоду", callback_data= "_"),
		types.InlineKeyboardButton(text = "Выбрать параметры", callback_data= "__")]

	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(*inbuttons)
	if message.from_user.id == AD:
		await message.answer(modules.messages.SETTINGS, reply_markup=keyboard)

#################Получение ответа от пользователя(город для погоды)
@dp.callback_query_handler(text="_")
async def input_city(call: types.CallbackQuery):

	await call.message.answer(text='Введи город: ')
	await dialog.otvet.set()

###################Помощь пользователям
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
	await message.reply(modules.messages.HELP, parse_mode='HTML')

##############Команда назад, возвращает нужную клавиатуру
@dp.message_handler(commands=['back'])
async def back(message: types.Message):
	await message.reply(f'Возвращаемся...', reply_markup=kb)



#################Проверка пользователя, является ли он админом
@dp.message_handler(commands=['admin'], is_chat_admin=True)
async def get_id_admin(message: types.Message):
	global AD
	AD = message.from_user.id
	await bot.send_message(message.from_user.id, 'Проверка связи;)', reply_markup=kb1)
	await message.reply('Ты админ, всё хорошо', reply_markup=kb1)



##################Ответ пользователю на полученное значение города(подтверждает город)
@dp.message_handler(state=dialog.otvet)
async def namee(message: types.Message, state: FSMContext):
	if message.from_user.id == AD:
		global name 
		name = message.text
		name = name[1:]
		await dialog.next()
		await message.reply(f'Твой город: {name}', reply_markup=kb)	
		
		return name


#################получает тответ пользователя на запрос о параметрах погоды
@dp.callback_query_handler(text="__")
async def input_city(call: types.CallbackQuery):
	await call.message.answer(text='Выбери параметры(1 - упрощённый режим, 2 - средний режим, 3 - нахуй тебе столько информации:): ')
	await call.message.reply("Для выбора напиши /цифра(1-3)", reply_markup=kb)
	await dialog.otvet_par.set()

@dp.message_handler(commands = ['param'])



#############Связь с сайтом погоды(от куда берётся информация)
@dp.message_handler(state=dialog.otvet_par)
async def namee(message: types.Message, state: FSMContext):
	param = message.text
	param = param[1:]
	await dialog.next()

		r = requests.get(
		f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={modules.config.OPENWEATHER_TOKEN}&units=metric"
		
		)
		data = r.json()

		class phar:
			def __init__(self, p1,p2,p3):
				self.p1 = p1
				self.p2 = p2
				self.p3 = p3

		ph1 = phar(
			data["main"]["temp"],
			data["main"]["humidity"],
			data["main"]["temp"]
			)
		
		
		await message.answer(
		f"***{datetime.datetime.now().strftime('%d.%m.%Y - %H:%M')}***\n"
		f"Температура: {ph1.p1} °C\n"
		f"Влажность воздуха: {ph1.p2}%\n"
		f"Скорость ветра: {ph1.p3} m/s\n"
		f"Хорошего дня!\n")

		r = requests.get(
		f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={modules.config.OPENWEATHER_TOKEN}&units=metric"
		
		)
		data = r.json()
		class phar2:
			def __init__(self, p1,p2,p3,p4,p5,p6):
				self.p1 = p1
				self.p2 = p2
				self.p3 = p3
				self.p4 = p4
				self.p5 = p5
				self.p6 = p6

		ph2 = phar2(
			data["main"]["temp"],
			data["main"]["humidity"],
			data["wind"]["speed"],
			data["main"]["pressure"], 
			datetime.datetime.fromtimestamp(data["sys"]["sunrise"]),
			datetime.datetime.fromtimestamp(data["sys"]["sunset"])
			)

		await message.answer(
		f"***{datetime.datetime.now().strftime('%d.%m.%Y - %H:%M')}***\n"
		f"Температура: {ph2.p1} °C\n"
		f"Влажность воздуха: {ph2.p2}%\n"
		f"Скорость ветра: {ph2.p3} m/s\n"
		f"Атмосферное давление: {ph2.p4} мм.рт.ст\n"
		f"Восход: {ph2.p5}\n"
		f"Заход: {ph2.p6}\n"
		f"Хорошего дня!\n")



		r = requests.get(
		f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={modules.config.OPENWEATHER_TOKEN}&units=metric"
		
		)
		data = r.json()
		
		class phar3:
			def __init__(self, p1,p2,p3,p4,p5,p6,p7):
				self.p1 = p1
				self.p2 = p2
				self.p3 = p3
				self.p4 = p4
				self.p5 = p5
				self.p6 = p6
				self.p7 = p7
		ph3 = phar3(
	 	data["main"]["temp"],
		data["main"]["humidity"],
		data["wind"]["speed"],
		data["main"]["pressure"], 
		datetime.datetime.fromtimestamp(data["sys"]["sunrise"]),
		datetime.datetime.fromtimestamp(data["sys"]["sunset"]),
		datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
		)
		await message.answer(
		f"***{datetime.datetime.now().strftime('%d.%m.%Y - %H:%M')}***\n"
		f"Температура: {ph3.p1} °C\n"
		f"Влажность воздуха: {ph3.p2}%\n"
		f"Скорость ветра: {ph3.p3} m/s\n"
		f"Атмосферное давление: {ph3.p4} мм.рт.ст\n"
		f"Восход: {ph3.p5}\n"
		f"Заход: {ph3.p6}\n"
		f"Дневное время: {ph3.p7}\n"
		f"Хорошего дня!\n")


		if param == "выход":
			await message.answer("Завершили")
			await dialog.next()

#@dp.message_handler(commands=['weather'])
#async def weather_get(message: types.Message):
#	r = requests.get(
#		f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={modules.config.OPENWEATHER_TOKEN}&units=metric"
#		
#		)
#	data = r.json()
#	mas_weather = []
#	mas_weather.append(data["main"]["temp"])
#	
#	mas_weather.append(data["main"]["humidity"])
#	
#	mas_weather.append(data["wind"]["speed"])
#	
#	mas_weather.append(data["main"]["pressure"])
#	
#	mas_weather.append(datetime.datetime.fromtimestamp(data["sys"]["sunrise"]))
#	
#	mas_weather.append(datetime.datetime.fromtimestamp(data["sys"]["sunset"]))
#	
#	mas_weather.append(datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"]))
#	 
#	await message.reply("Успешно загружены параметры города!")
	
#	await message.reply(
###		f"Влажность воздуха: {mas_weather[1]}%\n"
	#	f"Скорость ветра: {mas_weather[2]} m/s\n"
	#	f"Атмосферное давление: {mas_weather[3]} мм.рт.ст\n"
	#	f"Восход: {mas_weather[4]}\n"
	#	f"Заход: {mas_weather[5]}\n"
	#	f"Дневное время: {mas_weather[6]}\n"
	#	f"Хорошего дня!\n"
	#	)


###########Запуск пуллинга бота
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)	