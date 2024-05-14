from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.database.requests import (new_user, add_suggest, get_suggests,
                                                        send_asnwer, delete_suggest)

import app.keyboard as kb

# Create router
r = Router()

# States
class Stats_send_suggest(StatesGroup):
    suggest = State()

class Stats_answer(StatesGroup):
    sending_answer = State()

# Global values
suggest_current_id = 0

# Command Start
@r.message(Command('start'))
async def cmd_start(message: Message):
    await new_user(message.from_user.id, message.from_user.full_name)
    await message.answer(text=f'Привет, {message.from_user.full_name}, это предложка.\nЕсли ты хочешь что-то предложить вводи /suggest.\nЧто бы просмотреть все предложки пропишите /check_suggests')
    
# Command Suggest
@r.message(Command('suggest'))
async def cmd_send_suggest(message: Message, state: FSMContext):
    await state.set_state(Stats_send_suggest.suggest)
    await message.answer(text=f'Вводи свое предложение.\n(Лимит в 1000 символов)')
    
# Send Suggest
@r.message(Stats_send_suggest.suggest)
async def add_in_db(message: Message, state: FSMContext):
    if len(message.text) > 1000:
        await message.answer("К сожелению вы написали больше 1000 сообщений, попробуй сократить текст, и написать снова.")
        return -1
    await state.update_data(suggest=message.text)
    await add_suggest((await state.get_data())['suggest'],message.from_user.username,message.from_user.full_name)
    await message.answer(text=f'Хорошо, ваше предложение добавлено в список.\nКогда появится овтет мы вам пришлем\nЕсли захотите написать еще предложение, то напишите команду /suggest')
    await state.clear()
    
# Get all suggests
@r.message(Command('check_suggests'))
async def cmd_check_suggests(message: Message):
    current_suggest = (await get_suggests())[(suggest_current_id)]
    final_id = len(await get_suggests())
    await message.answer(f'''Кто написал: @{current_suggest.who_suggest_us}
                                        \nНик кто написал: {current_suggest.who_suggest_full_name}
                                        \nТекст: {current_suggest.suggest_text}
                                        \nНомер: {(suggest_current_id + 1)}/{len(await get_suggests())}''',
                        reply_markup = await kb.scroll_suggestion(suggest_current_id,final_id))
    
@r.callback_query(F.data == 'next')
async def cb_next(cb: CallbackQuery):
    suggest_current_id = int(str(str(cb.message.text.split('Номер')[-1]).split(' ')[-1]).split('/')[0])
    current_suggest = (await get_suggests())[(suggest_current_id)]
    final_id = len(await get_suggests())
    await cb.message.edit_text(text=f'''Кто написал: @{current_suggest.who_suggest_us}
                                        \nНик кто написал: {current_suggest.who_suggest_full_name}
                                        \nТекст: {current_suggest.suggest_text}
                                        \nНомер: {(suggest_current_id + 1)}/{final_id}''',
                        reply_markup = await kb.scroll_suggestion(suggest_current_id,final_id))
    
@r.callback_query(F.data == 'back')
async def cb_next(cb: CallbackQuery):
    suggest_current_id = int(str(str(cb.message.text.split('Номер')[-1]).split(' ')[-1]).split('/')[0]) - 2
    current_suggest = (await get_suggests())[(suggest_current_id)]
    final_id = len(await get_suggests())
    await cb.message.edit_text(text=f'''Кто написал: @{current_suggest.who_suggest_us}
                                        \nНик кто написал: {current_suggest.who_suggest_full_name}
                                        \nТекст: {current_suggest.suggest_text}
                                        \nНомер: {(suggest_current_id + 1)}/{final_id}''',
                        reply_markup = await kb.scroll_suggestion(suggest_current_id,final_id))
    
@r.callback_query(F.data == 'answer')
async def start_answer(cb: CallbackQuery, state: FSMContext):
    await state.set_state(Stats_answer.sending_answer)
    await state.update_data(text_suggest=cb.message.text)
    await cb.answer('')
    await cb.message.answer(text='Пишите ответ')
    
@r.message(Stats_answer.sending_answer)
async def answer_text_sending(message: Message, state: FSMContext):
    id_suggest = (int(str(str((await state.get_data())['text_suggest'].split('Номер')[-1]).split(' ')[-1]).split('/')[0]))
    await send_asnwer(((await get_suggests())[(id_suggest - 1)]),(message.text))
    current_suggest = (await get_suggests())[(suggest_current_id)]
    final_id = len(await get_suggests())
    await message.answer(f'''Кто написал: @{current_suggest.who_suggest_us}
                                        \nНик кто написал: {current_suggest.who_suggest_full_name}
                                        \nТекст: {current_suggest.suggest_text}
                                        \nНомер: {(suggest_current_id + 1)}/{len(await get_suggests())}''',
                        reply_markup = await kb.scroll_suggestion(suggest_current_id,final_id))
    await state.clear()
    
@r.callback_query(F.data == 'delete')
async def cb_next(cb: CallbackQuery):
    id_suggest = (int(str(str(cb.message.text.split('Номер')[-1]).split(' ')[-1]).split('/')[0]) - 1)
    await delete_suggest(id_suggest)