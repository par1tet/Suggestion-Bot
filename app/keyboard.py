from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def scroll_suggestion(current_id,final_id):
    keyboard = InlineKeyboardBuilder()
    if current_id != 0 and not (current_id == final_id - 1):
        keyboard.add(InlineKeyboardButton(text=f'Назад {current_id}', callback_data='back'))
        keyboard.add(InlineKeyboardButton(text=f'Дальше {current_id+2}', callback_data='next'))
        keyboard.add(InlineKeyboardButton(text=f'Ответить', callback_data='answer'))
        return keyboard.adjust(2).as_markup()
    elif current_id == final_id - 1:
        keyboard.add(InlineKeyboardButton(text=f'Назад {current_id}', callback_data='back'))
        keyboard.add(InlineKeyboardButton(text=f'Ответить', callback_data='answer'))
        return keyboard.adjust(1).as_markup()
    else:
        keyboard.add(InlineKeyboardButton(text=f'Дальше {current_id+1}', callback_data='next'))
        keyboard.add(InlineKeyboardButton(text=f'Ответить', callback_data='answer'))
        return keyboard.adjust(1).as_markup()