from aiogram import Dispatcher, types

from DataBase import database
from textpad import * 
from keyboards import * 
from payment import * 
from init import dp, bot 
from config import PAYMENT
from MachineState import MachineState

##################################################################
# PREVIOUS AND NEXT MACHIN STATE

async def MS_move(callback: types.CallbackQuery):
    match callback.data:
        case 'previous':
            await MachineState.previous()
        case 'next':
            await MachineState.next()
    await callback.answer()
    await next_func(callback)

# WELCOME

async def welcome(callback: types.CallbackQuery):
    n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
    if n['state'] is None:
        await callback.message.edit_text(text_inline_start, reply_markup=start_keyboard)

# ABOUT

async def channel(callback: types.CallbackQuery):
    n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
    if n['state'] == 'MachineState:About':
        await callback.message.edit_text(text_inline_about, reply_markup=about_keyboard)

# BACK

async def back(callback: types.CallbackQuery):
    await next_func(callback)

# PLAN LIST

async def plan(callback: types.CallbackQuery):
    n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
    if n['state'] == 'MachineState:List':
        await callback.message.edit_text(text_plan_main, reply_markup=plan_keyboard)
        await callback.answer()

async def plan_list(callback: types.CallbackQuery):
    n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
    if n['state'] == 'MachineState:List':
        plans = database.plan_save(callback.message)
        if plans is None:
            return await callback.message.edit_text('Вы ещё не создали список дел', reply_markup=back_keyboard)
        else:
            await callback.message.edit_text(text_plan_list + plans[2].keys(), reply_markup=back_keyboard)
        await callback.answer()

# DELETE MESSAGE

async def delete(callback:types.CallbackQuery):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.answer()

async def next_func(callback):
    await welcome(callback)
    await correct(callback)
    await channel(callback)
    await plan(callback)

def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(MS_move, text=['previous', 'next'], state='*')
    dp.register_callback_query_handler(delete, text='del', state='*')
    dp.register_callback_query_handler(back, text='back', state='*')
    dp.register_callback_query_handler(welcome, state=None)
    dp.register_callback_query_handler(channel, text='channel', state=MachineState.About)
    dp.register_callback_query_handler(plan_list, text='plan', state=MachineState.List)
    dp.register_callback_query_handler(plan, state=MachineState.List)