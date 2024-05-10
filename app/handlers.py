from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.database.requests import new_user

#Create router
r = Router()

#States
class Reg(StatesGroup):
    suggest = State()

#Command Start
@r.message(Command('start'))
async def cmd_start(message: Message):
    await new_user(message.from_user.id, message.from_user.full_name)
    await message.answer(text=f'Привет, {message.from_user.full_name}, это предложка.\nЕсли ты хочешь что-то предложить вводи /suggest.')
    
#Command Suggest
@r.message(Command('suggest'))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Reg.suggest)
    await message.answer(text=f'Вводи свое предложение.\n(Лимит в 1000 символов)')
    
#Get Suggest
@r.message(Reg.suggest)
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(suggest=message.text)
    print((await state.get_data())['suggest'])
    await message.answer(text=f'Хорошо, ваше предложение добавлено в список.')
    await state.clear()