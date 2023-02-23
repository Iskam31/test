from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
#kb.add(types.InlineKeyboardButton(text="/start"))
#kb.add(types.InlineKeyboardButton(text="/Помощь")).insert(types.InlineKeyboardButton('/Показать погоду'))
#kb.add(types.InlineKeyboardButton(text="/->Настройки(adm)->")).insert(types.InlineKeyboardButton('/Убрать клавиатуру'))


kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
kb1.insert(KeyboardButton('/back')).insert(KeyboardButton('/inpWeather'))

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.insert(KeyboardButton('***'))
kb.insert(KeyboardButton('/weather')).insert(KeyboardButton('/help'))
kb.insert(KeyboardButton('/settings')).insert(KeyboardButton('???'))
