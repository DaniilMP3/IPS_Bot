from create_bot import dp
from aiogram import executor
from start import register_start_handler
from schedule import register_schedule_handler
from admin import register_admin_handlers


async def on_startup(_):
    print('Online')
    register_admin_handlers(dp)
    register_start_handler(dp)
    register_schedule_handler(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


