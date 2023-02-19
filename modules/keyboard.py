from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

defaultKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
defaultKeyboard.insert(KeyboardButton('/weather')).insert(KeyboardButton('/help'))
