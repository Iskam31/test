from aiogram import Bot, Dispatcher, executor, types
API_TOKEN = '6083003984:AAHXRKN8zxyBlyLMjJkAgoD99RytkijFs7o'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply("Привет бот, я бот ;)\nОтправь мне любое сообщение, я постараюсь ответить")
@dp.message_handler()
async def echo(message: types.Message):
	await message.answer(message.text)
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)