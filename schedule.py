from create_bot import bot, AVAILABLE_DAYS
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
import json
from keyboards import day_schedule_keyboard, user_keyboard, get_keyboard
from aiogram.dispatcher import FSMContext


async def show_schedule(message):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    with open('schedule.json', 'r') as file:
        schedule_dict = json.load(file)
    day = message.text.split('_')[1].lower()
    if day in AVAILABLE_DAYS:
        if day in schedule_dict:
            schedule_message = schedule_dict[day]['message']
            entities = [types.MessageEntity(type=entity['type'],
                                            offset=entity['offset'],
                                            length=entity['length'],
                                            url=entity['url']) for entity in schedule_dict[day]['entities']]

            if message.chat.type == 'private':
                await bot.send_message(chat_id, schedule_message, entities=entities,
                                        reply_markup=await get_keyboard(user_id))
            else:
                await bot.send_message(chat_id, schedule_message, entities=entities)
        else:
            if message.chat.type == 'private':
                await bot.send_message(chat_id, "There's no lessons this day.", reply_markup=await get_keyboard(user_id))
            else:
                await bot.send_message(chat_id, "There's no lessons this day.")

    else:
        if message.chat.type == 'private':
            await bot.send_message(chat_id, 'Incorrect day', reply_markup=await get_keyboard(user_id))
        else:
            await bot.send_message(chat_id, 'Incorrect day')


async def show_days(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    await state.set_state('schedule_choose_day')
    await bot.send_message(chat_id, 'Choose day:', reply_markup=day_schedule_keyboard)


async def show_schedule_private(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    if message.text == '❌':
        await bot.send_message(chat_id, 'You canceled choosing.', reply_markup=await get_keyboard(user_id))
    else:
        await show_schedule(message)
    await state.finish()


async def show_schedule_group(message: types.Message):
    await show_schedule(message)







def register_schedule_handler(dp: Dispatcher):
    dp.register_message_handler(show_days, Text(equals=['/Schedule']), chat_type=[types.ChatType.PRIVATE])
    dp.register_message_handler(show_schedule_private, state='schedule_choose_day')
    dp.register_message_handler(show_schedule_group, Text(startswith=['/Schedule_']))
