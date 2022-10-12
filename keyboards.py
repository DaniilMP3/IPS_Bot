from aiogram import types
from create_bot import ADMINS

user_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(
            '/Schedule'), types.KeyboardButton('/Homework'))

admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(
                '/Schedule'), types.KeyboardButton('/Homework'), types.KeyboardButton('/Edit_Schedule'))


async def get_keyboard(user_id):
    if user_id in ADMINS:
        return admin_keyboard
    else:
        return user_keyboard


admin_choose_day_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('/Schedule_Monday'),
        types.KeyboardButton('Tuesday'),
        types.KeyboardButton('Wednesday'),
        types.KeyboardButton('Thursday'),
        types.KeyboardButton('Friday'),
        types.KeyboardButton('Saturday'),
        types.KeyboardButton('Sunday'),
        types.KeyboardButton('❌'))

day_schedule_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('/Schedule_Monday'),
        types.KeyboardButton('/Schedule_Tuesday'),
        types.KeyboardButton('/Schedule_Wednesday'),
        types.KeyboardButton('/Schedule_Thursday'),
        types.KeyboardButton('/Schedule_Friday'),
        types.KeyboardButton('/Schedule_Saturday'),
        types.KeyboardButton('/Schedule_Sunday'),
        types.KeyboardButton('❌'))
