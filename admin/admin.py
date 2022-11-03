from aiogram import types, Dispatcher
from custom_filters import IsAdmin
from aiogram.dispatcher import FSMContext
from keyboards import admin_keyboard, admin_choose_day_keyboard, lessons_keyboard, single_cross_kb
from aiogram.dispatcher.filters import Text
from create_bot import AVAILABLE_DAYS, schedule_dict, bot, LESSONS_TIME
from aiogram.dispatcher.filters.state import State, StatesGroup
import json
from time import strptime


async def update_schedule(message, data, day, lesson):
    msg = ''
    if day not in schedule_dict:
        schedule_dict[day] = {'lessons': {lesson: data}, 'message': ''}

    if day in schedule_dict:
        schedule_dict[day]['lessons'][lesson] = data
        for i in sorted(schedule_dict[day]['lessons']):
            msg += schedule_dict[day]['lessons'][i]['message']
            msg += '\n'

    print(msg)



    message_with_entities = message.parse_entities(as_html=True)


    # async def construct_string():
    #     msg = ''
    #     # print(sorted(schedule_dict[day]['lessons']))
    #     for i in sorted(schedule_dict[day]['lessons']):
    #         msg += schedule_dict[day]['lessons'][i]['message']
    #         msg += '\n'
    #     return msg
    #
    # message_with_entities = message.parse_entities(as_html=True)
    #
    # schedule_dict[day]['lessons'][lesson] = {'message': message_with_entities}
    #
    # schedule_dict[day]['message'] = ''
    # schedule_dict[day]['message'] += await construct_string()
    #
    # await construct_string()
    # with open('schedule.json', 'w', encoding='utf-8') as file:
    #     json.dump(schedule_dict, file)


class Schedule(StatesGroup):
    day = State()
    lesson = State()
    lesson_info = State()

    start_time = State()
    end_time = State()

    create_lesson = State()
    delete_lesson = State()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    if message.text == '❌':
        await state.finish()
        await message.reply('Cancelled.', reply_markup=admin_keyboard)


async def start_edit(message: types.Message):
    await Schedule.day.set()
    chat_id = str(message.chat.id)

    await bot.send_message(chat_id, 'Choose day:', reply_markup=admin_choose_day_keyboard)


async def choose_day(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    if message.text.lower() in AVAILABLE_DAYS:

        # if message.text.lower() not in schedule_dict:
        #     schedule_dict[message.text.lower()] = {'lessons': {}} ###if day not in dict yet - add it

        await state.update_data(day=message.text.lower())
        await Schedule.next() ### choose lesson

        lessons_kb = await lessons_keyboard(message.text.lower())
        await bot.send_message(chat_id, 'Choose or create a new lesson:', reply_markup=lessons_kb)
    else:
        await bot.send_message(chat_id, 'Incorrect day')


async def choose_lesson(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    async with state.proxy() as data:
        day = data['day']
    ###Delete or create cases
    if message.text.lower() == 'create':
        await bot.send_message(chat_id, "Enter a lesson number:", reply_markup=single_cross_kb)
        await Schedule.create_lesson.set() ### go to create_lesson
        return
    elif message.text.lower() == 'delete':
        if day in schedule_dict:
            await bot.send_message(chat_id, "Choose lesson to delete:", reply_markup=await lessons_keyboard(day, only_lessons=True))
            await Schedule.delete_lesson.set()
            return
        await bot.send_message(chat_id, 'Nothing to delete.', reply_markup=await lessons_keyboard(day))
        return
    ###Delete or create cases

    if day in schedule_dict: ###message.text  -  lesson(1,2,3...)
        if message.text in schedule_dict[day]['lessons']:
            ###send ex lesson info if in dict
            await bot.send_message(chat_id, f"Info about this lesson, you can copy it if you need:\n{schedule_dict[day]['lessons'][message.text]['message']}",
                                   reply_markup=single_cross_kb)
            await state.update_data(lesson=message.text)
            await Schedule.next()

        else:
            await bot.send_message(chat_id, "This lesson is not exist, but you can create it.")


async def delete_lesson(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    async with state.proxy() as data:
        day = data['day']
    if message.text in schedule_dict[day]['lessons']:
        del schedule_dict[day]['lessons'][message.text]
        await bot.send_message(chat_id, 'You successfully delete a lesson', reply_markup=admin_keyboard)

        with open('schedule.json', 'w', encoding='utf-8') as file:
            json.dump(schedule_dict, file)
        await state.finish()

    else:
        await bot.send_message(chat_id, "Not-existent lesson.")


async def create_lesson(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    async with state.proxy() as data:
        day = data['day']

    if day in schedule_dict:
     ###if admin trying to create more than 6 lessons
        if len(schedule_dict[day]['lessons']) == 6:
            await bot.send_message(chat_id, 'You can not create more than 6 lessons.')
            return

    if message.text.isdigit():
        if message.text not in '123456':
            await bot.send_message(chat_id, 'You can create 1-6 lessons only.')
            return

        await state.update_data(lesson=message.text)

        # if message.text in LESSONS_TIME: ###if this lesson in common lessons time - show it
        #     await bot.send_message(chat_id, f'Now enter start time, for {message.text} lesson. Probably, it is - {LESSONS_TIME[message.text]["start"]}',
        #                            reply_markup=single_cross_kb)
        # else:
        #     await bot.send_message(chat_id, 'Now a lesson info.', reply_markup=single_cross_kb)
        await bot.send_message(chat_id, "Enter the lesson info", reply_markup=single_cross_kb)

        await Schedule.lesson_info.set()


async def lesson_info(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    await state.update_data(lesson_info=message.text)
    await bot.send_message(chat_id, "Now enter a start time.")
    await Schedule.next()


async def start_time(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    try:
        strptime(message.text, '%H:%M:%S') ### if format is incorrect - there will be value error and except block starts work

        await state.update_data(start=message.text)
        await bot.send_message(chat_id, 'Now enter the end time:')
        await Schedule.end_time.set()
    except ValueError:
        await bot.send_message(chat_id, 'Incorrect format')


async def end_time(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    try:
        async with state.proxy() as data:
            start = data['start']

        strptime(message.text, '%H:%M:%S')

        if message.text < start:
            await bot.send_message(chat_id, 'You can not send less time than start time.')
        elif message.text == start:
            await bot.send_message(chat_id, 'You can not send the same as start_time')
        else:

            async with state.proxy() as data:
                day = data['day']
                lesson = data['lesson']
                lesson_inf = data['lesson_info']

            end = message.text
            data = {'start': start, 'end': end, 'message': lesson_inf}

            await update_schedule(message, data, day, lesson)
            await bot.send_message(chat_id, 'You successfully edit a lesson.', reply_markup=admin_keyboard)
            await state.finish()

    except ValueError:
        await bot.send_message(chat_id, 'Incorrect format')


async def start_change(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    await bot.send_message(chat_id, '1.Edit lesson info'
                                    '2.Edit start time'
                                    '3.Edit end time')



def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(start_edit, IsAdmin(), Text(equals=['/Edit_Schedule']), state=None),
    dp.register_message_handler(cancel_handler, IsAdmin(), Text(equals=['❌']), state='*')
    dp.register_message_handler(choose_day, state=Schedule.day)
    dp.register_message_handler(choose_lesson, state=Schedule.lesson)
    dp.register_message_handler(create_lesson, state=Schedule.create_lesson)
    dp.register_message_handler(delete_lesson, state=Schedule.delete_lesson)
    dp.register_message_handler(start_time, state=Schedule.start_time)
    dp.register_message_handler(end_time, state=Schedule.end_time)
    dp.register_message_handler(lesson_info, state=Schedule.lesson_info)
