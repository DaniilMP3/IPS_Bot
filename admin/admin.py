from aiogram import types, Dispatcher
from json_operations import write_in_json
from custom_filters import IsAdmin
from create_bot import bot
from aiogram.dispatcher import FSMContext
from keyboards import admin_keyboard, admin_choose_day_keyboard
from aiogram.dispatcher.filters import Text
from create_bot import AVAILABLE_DAYS


async def start_edit(message: types.Message, state: FSMContext):
    await state.set_state('admin_choose_day')
    chat_id = str(message.chat.id)

    await bot.send_message(chat_id, 'Choose day:', reply_markup=admin_choose_day_keyboard)


async def choose_day(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    if message.text == '❌':
        await state.finish()
        await bot.send_message(chat_id, 'You canceled editing.', reply_markup=admin_keyboard)

    else:
        if message.text.lower() in AVAILABLE_DAYS:
            async with state.proxy() as data:
                data['day'] = message.text.lower()

            await state.set_state('wait_for_message')
            await bot.send_message(chat_id, 'Enter schedule:', reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                types.KeyboardButton('❌')
            ))
        else:
            await bot.send_message(chat_id, 'Incorrect day', reply_markup=admin_choose_day_keyboard)


async def edit_schedule_day(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    async with state.proxy() as data:
        day = data['day']

    if message.text == '❌':
        await state.finish()
        await bot.send_message(chat_id, 'You canceled editing', reply_markup=admin_keyboard)

    else:
        await state.finish()
        await write_in_json(day, message)
        await bot.send_message(chat_id, 'You successfully changed schedule.', reply_markup=admin_keyboard)





def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(start_edit, IsAdmin(), Text(equals=['/Edit_Schedule']))
    dp.register_message_handler(choose_day, state='admin_choose_day')
    dp.register_message_handler(edit_schedule_day, state='wait_for_message')
