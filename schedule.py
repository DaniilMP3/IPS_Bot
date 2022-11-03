from create_bot import bot, AVAILABLE_DAYS, schedule_dict
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
import json
from keyboards import day_schedule_keyboard, user_keyboard, get_keyboard
from aiogram.dispatcher import FSMContext
from datetime import datetime


async def show_schedule(message, day, show_current=False):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    chat_type = message.chat.type

    if day in AVAILABLE_DAYS:
        if day in schedule_dict:
            schedule_message = schedule_dict[day]['message']

            await bot.send_message(chat_id, schedule_message, parse_mode='HTML', reply_markup=await get_keyboard(user_id, chat_type))
        else: ###if admin do not edit sth for this day
            await bot.send_message(chat_id, "There's no lessons today.", reply_markup=await get_keyboard(user_id,
                                                                                                            chat_type))

    else:
        await bot.send_message(chat_id, 'Incorrect day', reply_markup=await get_keyboard(user_id,
                                                                                         chat_type))


async def show_days(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    await state.set_state('schedule_choose_day')
    await bot.send_message(chat_id, 'Choose day:', reply_markup=day_schedule_keyboard)


async def show_schedule_private(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    chat_type = message.chat.type
    day = message.text.split('_')[1].lower().split('@')[0]
    if message.text == '❌':
        await bot.send_message(chat_id, 'You canceled choosing.', reply_markup=await get_keyboard(user_id, chat_type))
    else:
        await show_schedule(message, day)
    await state.finish()


async def show_schedule_group(message: types.Message):
    day = message.text.split('_')[1].lower().split('@')[0]
    await show_schedule(message, day)



async def show_today_schedule(message: types.Message):
    day = datetime.now().strftime('%A').lower()
    await show_schedule(message, day)


async def show_current_lesson(message: types.Message):
    datetime_instance = datetime.now()
    day = datetime_instance.strftime('%A').lower()
    await show_schedule(message, day, show_current=True)


def register_schedule_handler(dp: Dispatcher):
    dp.register_message_handler(show_days, Text(equals=['/Schedule']), chat_type=[types.ChatType.PRIVATE])
    dp.register_message_handler(show_schedule_private, state='schedule_choose_day')
    dp.register_message_handler(show_today_schedule, Text(startswith=['/schedule_today']))
    dp.register_message_handler(show_schedule_group, Text(startswith=['/schedule_']))
    dp.register_message_handler(show_current_lesson, Text(startswith=['/now']))
