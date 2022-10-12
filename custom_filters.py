from aiogram.types import Message
from aiogram.dispatcher.filters import Filter
from create_bot import ADMINS


class IsAdmin(Filter):
    async def check(self, message: Message):
        return str(message.from_user.id) in ADMINS and message.chat.type == 'private'
