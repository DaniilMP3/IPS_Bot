from aiogram import types
from create_bot import ADMINS, schedule_dict

user_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(
            '/Schedule'), types.KeyboardButton('/Homework'))

admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(
                '/Schedule'), types.KeyboardButton('/Homework'), types.KeyboardButton('/Edit_Schedule'))

single_cross_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add('❌')


async def get_keyboard(user_id, chat_type):
    if chat_type == 'private':
        if user_id in ADMINS:
            return admin_keyboard
        else:
            return user_keyboard
    return None


async def lessons_keyboard(day, only_lessons=False):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if day in schedule_dict:
        for lesson in sorted(schedule_dict[day]['lessons']):
            kb.add(f"{lesson}")

    if only_lessons is True:
        kb.add('❌')
        return kb
    kb.add('Create')
    kb.add('Delete')
    kb.add('❌')
    return kb

admin_choose_day_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Monday'),
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
