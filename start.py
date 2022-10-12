from aiogram import types, Dispatcher
from create_bot import bot, ADMINS
from keyboards import user_keyboard, admin_keyboard


async def start(message: types.Message):
    chat_id = str(message.chat.id)
    if message.chat.type == 'private':

        if str(message.from_user.id) in ADMINS:
            await bot.send_message(chat_id, "ІПС-12 bot-helper. You can edit schedule and homework:)",
                                   reply_markup=admin_keyboard)
        else:
            await bot.send_message(chat_id, "ІПС-12 bot-helper:)", reply_markup=user_keyboard)


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
