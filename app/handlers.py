from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

#Create router
r = Router()

#Command Start
@r.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(text=f'Привет, f{message.from_user.full_name}, это предложка.\nЕсли ты хочешь что то предложить то напиши команду /suggest, а потом предложение.')