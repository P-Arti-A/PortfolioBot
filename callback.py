from aiogram import Dispatcher, types, utils
from datetime import datetime

from DataBase import database
from textpad import * 
from keyboards import * 
from payment import * 
from init import dp, bot 
from config import PAYMENT
from MachineState import MachineState, MachineState_1

##################################################################
# PREVIOUS AND NEXT MACHIN STATE

async def MS_move(callback: types.CallbackQuery):
    match callback.data:
        case 'previous':
            try:
                n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
                await MachineState.previous()
                if n['state'] is None:
                    await MachineState.last()
                # elif n['state'] == 'MachineState:Excel':
                #     await MachineState.List.set()
                # else:   
            except KeyError:
                await MachineState.Start.set()
                await MachineState.previous()
        case 'next':
            try:
                n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
                await MachineState.next()
                if n['state'] is None:
                    await MachineState.first()
                # if n['state'] == 'MachineState:List':
                #     await MachineState.Excel.set()
                # else:
            except KeyError:
                await MachineState.Start.set()
                await MachineState.next()
    await callback.answer()
    await next_func(callback)

##################################################################
# CLASS FOR CARDREADER

async def MS_data(callback:types.CallbackQuery, state:str):
    try:
        n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
        if n['state'] == state:
            return True
    except KeyError as e:
        print('Ошибка машины состояний: '+ str(e))
    except utils.exceptions.MessageNotModified as e:
        print('Ошибка изменения сообщения: '+ str(e))
    return False


# WELCOME

async def welcome(callback: types.CallbackQuery):
    if await MS_data(callback, state='MachineState:Start'):
        await callback.message.edit_text(text_inline_start, reply_markup=start_keyboard)

# ABOUT

async def channel(callback: types.CallbackQuery):
    if await MS_data(callback, 'MachineState:About'):
        if callback.data != 'channel':
            await callback.message.edit_text(text_inline_about, reply_markup=about_keyboard)
        else:
            await callback.message.edit_text(text_inline_command_about, reply_markup=start_keyboard)
    await callback.answer()
# BACK

async def back(callback: types.CallbackQuery):
    if await MS_data(callback, 'MachineState_1:List_main'):
        await MachineState.List.set()
    await next_func(callback)

# PLAN LIST

async def backworklist(callback: types.CallbackQuery):
    await plan_list(callback)

async def worklist_update(callback: types.CallbackQuery):
    await worklist(callback, update=True)

async def plan_update(callback: types.CallbackQuery):
    await plan_list(callback, update=True)

async def worklist(callback: types.CallbackQuery, update:bool = False):
    await MachineState_1.List_create.set()
    lists = database.plan_save(callback.message, plan_title_cor=None if update else callback.data[5:])
    try:
        if lists[2][lists[3]] is None:
            await callback.message.edit_text(f'_{lists[3]}_\n\nСписок пуст.\nНапишите первую задачу', reply_markup=back_update_worklist_keyboard, parse_mode='Markdown')
        else:
            # date = datetime.now()
            await callback.message.edit_text(f'_{lists[3]}_\n\n' + '\n'.join([str(x)+'. '+y for x, y in enumerate(lists[2][lists[3]], 1)]), reply_markup=back_update_worklist_keyboard, parse_mode='Markdown')
    except utils.exceptions.MessageNotModified:
        pass
    except KeyError:
        await callback.message.edit_text(f'Список _{lists[3]}_ был удалён.\nНапишите кнопку "Назад"', reply_markup=back_worklist_keyboard, parse_mode='Markdown')
    if update:
        await callback.answer('Обновлено!')

async def plan(callback: types.CallbackQuery):
    if await MS_data(callback, 'MachineState:List'):
        await callback.message.edit_text(text_plan_main, reply_markup=plan_keyboard)
        await callback.answer()

async def plan_list(callback: types.CallbackQuery, update:bool=False):
    await MachineState_1.List_main.set()
    plans = database.plan_save(callback.message)
    try:
        if plans is None or len(plans[2]) == 0:
            await callback.message.edit_text(text_plan_list + '\n\nВы ещё не создали список задач', reply_markup=back_update_keyboard)
        else:
            await callback.message.edit_text(text_plan_list + '\n\n' + 'Ваши списки дел:\n' + '\n'.join([str(x)+'. '+y for x, y in enumerate([i for i in plans[2].keys()], 1)]), reply_markup=WorkKeybords(callback))
    except utils.exceptions.MessageNotModified:
        pass
    if update:
        await callback.answer('Обновлено!')
    else:
        await callback.answer()

# WEB

async def web(callback: types.CallbackQuery):
    if await MS_data(callback, 'MachineState:Web'):
        await callback.message.edit_text(text_web, reply_markup=web_keyboard)
        await callback.answer()
   
# FF

# async def FF(callback: types.CallbackQuery):
#     if await MS_data(callback, 'MachineState:FF'):
#         await callback.message.edit_text(text_FF, reply_markup=start_keyboard)
#         await callback.answer()

# DELETE MESSAGE

async def delete(callback:types.CallbackQuery):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.answer()

async def next_func(callback):
    await welcome(callback)
    await correct(callback)
    await channel(callback)
    await plan(callback)
    await web(callback)
    # await FF(callback)

def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(MS_move, text=['previous', 'next'], state='*')
    dp.register_callback_query_handler(delete, text='del', state='*')
    dp.register_callback_query_handler(back, text='back', state='*')
    dp.register_callback_query_handler(backworklist, text='back_worklist', state=MachineState_1.List_create)
    dp.register_callback_query_handler(worklist_update, text='update_worklist', state=MachineState_1.List_create)
    dp.register_callback_query_handler(worklist, lambda text: 'list_' in text.data, state=MachineState_1.List_main)
    dp.register_callback_query_handler(channel, text='channel', state=MachineState.About)
    dp.register_callback_query_handler(plan_list, text='plan', state=MachineState.List)
    dp.register_callback_query_handler(plan_update, text='update_plan', state=MachineState_1.List_main)
    dp.register_callback_query_handler(welcome, state=MachineState.Start)
    dp.register_callback_query_handler(plan, state=MachineState.List)
    dp.register_callback_query_handler(web, state=MachineState.Web)
    # dp.register_callback_query_handler(FF, state=MachineState.FF)