# Internal library

import asyncio
import json

# External library for Telegram

import sqlite3
from aiogram import Bot, Dispatcher, executor, types, utils
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Library current project

from keyboards import *
from config import *

# Naming

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

Price1 = types.LabeledPrice('Подписка!', 10000)
Price2 = types.LabeledPrice('А вообще', 10000)
Price3 = types.LabeledPrice('Здесь может быть написано что угодно', 10000)

# Machine State

class MachineState (StatesGroup):
    About = State()
    Payment = State()
    List = State()
    Excel = State()
    FF = State()

##################################################################
# DataBase

db = sqlite3.connect('./DataFrame.db')  
cdb = db.cursor()
cdb.execute("""CREATE TABLE IF NOT EXISTS user (
	id	            INTEGER,
	user_id	        BIGINT,
	user_first_name	TEXT,
	user_username	TEXT,
	user_message_id	TEXT,
	PRIMARY KEY(id AUTOINCREMENT))
""")
cdb.execute("""CREATE TABLE IF NOT EXISTS plan (
	plan_id	        INTEGER ,
	user_id	        BIGINT,
	plan_title  	NUMERIC,
	plan_title_cor 	TEXT,
	plan_date   	TEXT,
    plan_date_notif	INTEGER,
	PRIMARY KEY(plan_id AUTOINCREMENT),
    FOREIGN KEY(user_id) REFERENCES user (user_id))
""")
db.commit()

# FUNCTION FOR SAVING USER INFORMATION

def data_save(message: types.Message, message_id: str = None) -> list: 
    cdb.execute(f'SELECT user_id FROM user WHERE user_id = {message.chat.id}')
    if cdb.fetchone() is None:
        cdb.execute (f"INSERT INTO user (user_id, user_first_name, user_username, user_message_id) VALUES (?, ?, ?, ?)", 
            (message.chat.id, message.chat.first_name, message.chat.username, message_id))
    else:
        cdb.execute (f"UPDATE user SET user_id = ?, user_first_name = ?, user_username = ?", 
            (message.chat.id, message.chat.first_name, message.chat.username))
    if message_id is not None:
        cdb.execute (f"UPDATE user SET user_message_id = ?", (message_id, ))
    db.commit()
    cdb.execute(f'SELECT * FROM user WHERE user_id = {message.chat.id}')
    return cdb.fetchone()

# FUNCTION FOR SAVING WORK PLANS

def plan_save(message: types.Message, plan_title: dict = None, plan_title_cor: str = None, plan_date: str = None, plan_date_notif: int = None) -> list: 
    cdb.execute(f'SELECT user_id FROM plan WHERE user_id = {message.chat.id}')
    if cdb.fetchone() is None:
        cdb.execute(f'INSERT INTO plan (user_id) SELECT user_id FROM user WHERE user_id = {message.chat.id}')
    if plan_title is not None:
        cdb.execute (f"UPDATE plan SET plan_title = ?", (json.dumps(plan_title), ))
    if plan_title_cor is not None:
        cdb.execute (f"UPDATE plan SET plan_title_cor = ?", (plan_title_cor, ))
    if plan_date is not None:
        cdb.execute (f"UPDATE plan SET plan_date = ?", (plan_date, ))
    if plan_date_notif is not None:
        cdb.execute (f"UPDATE plan SET plan_date_notif = ?", (plan_date_notif, ))
    db.commit()
    cdb.execute(f'SELECT * FROM plan WHERE user_id = {message.chat.id}')
    exist = list(cdb.fetchone())
    try:
        exist[2] = json.loads(exist[2])
    except AttributeError:
        pass
    return exist

##################################################################
# PREVIOUS AND NEXT MACHIN STATE

@dp.callback_query_handler(text=['previous', 'next'], state='*')
async def MS_move(callback: types.CallbackQuery):
    match callback.data:
        case 'previous':
            await MachineState.previous()
        case 'next':
            await MachineState.next()
    await callback.answer()
    await next_func(callback)

##################################################################
# Inline Handlers

# WELCOME

@dp.callback_query_handler(state=None)
async def welcome(callback: types.CallbackQuery):
    n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
    if n['state'] is None:
        await callback.message.edit_text(text_inline_start, reply_markup=start_keyboard)

# ABOUT

@dp.callback_query_handler(text='channel', state=MachineState.About)
async def channel(callback: types.CallbackQuery):
    n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
    if n['state'] == 'MachineState:About':
        await callback.message.edit_text(text_inline_about, reply_markup=about_keyboard)

# BACK

@dp.callback_query_handler(text='back', state='*')
async def back(callback: types.CallbackQuery):
    await next_func(callback)

# DETAILS AND BUY PASS 

@dp.callback_query_handler(text=['buy', 'other'], state=MachineState.Payment)
async def correct(callback:types.CallbackQuery):
    n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
    if n['state'] == 'MachineState:Payment':
        if callback.data == 'buy':
            await bot.send_invoice(callback.message.chat.id, 
                title=text_invoice_title, 
                description=text_invoice_description,
                provider_token=PAYMENT2,
                currency='rub',
                prices=[Price1, Price2, Price3],
                payload='test_payload',
                start_parameter='subscribe',
                reply_markup=delete_keyboard)
        elif callback.data == 'other':
            await callback.message.edit_text(text_callback_other, reply_markup=buy_vote)
        else:

            await callback.message.edit_text(text_inline_payment, reply_markup=buy_vote)
        await callback.answer()

# PLAN LIST

@dp.callback_query_handler(state=MachineState.List)
async def plan(callback: types.CallbackQuery):
    n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
    if n['state'] == 'MachineState:List':
        await callback.message.edit_text(text_plan_main, reply_markup=plan_keyboard)
        await callback.answer()

@dp.callback_query_handler(text='plan', state=MachineState.List)
async def plan_list(callback: types.CallbackQuery):
    n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
    if n['state'] == 'MachineState:List':
        plans = plan_save(callback.message)
        if plans is None:
            return await callback.message.edit_text('Вы ещё не создали список дел', reply_markup=back_keyboard)
        else:
            await callback.message.edit_text(text_plan_list + plans[2].keys(), reply_markup=back_keyboard)
        await callback.answer()

# DELETE MESSAGE

@dp.callback_query_handler(text='del', state='*')
async def delete(callback:types.CallbackQuery):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.answer()


##################################################################
# Handlers pre checkout payment

@dp.pre_checkout_query_handler(lambda query: True, state='*')
async def pre_checkout_query(checkout: types.ShippingQuery):
    await bot.answer_pre_checkout_query(checkout.id, True)

# Handlers SUCCESSFUL PAYMENT

@dp.message_handler(content_types=types.message.ContentType.SUCCESSFUL_PAYMENT, state='*')
async def successful_pay(message: types.Message):
    pay_info = message.successful_payment.to_python()
    for k, v in pay_info.items():
        print(k, v, sep=' ')
    delet = await message.answer(f'Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} от [{message.chat.first_name}](t.me/{message.from_user.username}), прошел успешно (Сообщение удалиться через 30 секунд)',
                        parse_mode='Markdown', 
                        disable_web_page_preview=True)
    await asyncio.sleep(30)
    await bot.delete_message(message.chat.id, delet.message_id)

##################################################################
# Handlers

# START

@dp.message_handler(commands='start', state='*')
async def start(message: types.Message):
    user = data_save(message)
    if user[-1] is not None:
        try:
            await bot.delete_message(message.chat.id, user[-1])
        except:
            pass
    await bot.delete_message(message.chat.id, message.message_id)
    message_id = await bot.send_message(message.chat.id, text_inline_start, reply_markup=start_keyboard)
    data_save(message, message_id.message_id)

# CREATE WORK PLANS

@dp.message_handler(commands='create', state=MachineState.List)
async def plan_text(message: types.Message):
    plans = plan_save(message)
    new_plan = plans[2].get(message.text[8:], None)
    if plans[2] is None:
        new_plan = {message.text[8:]: None}
        print(new_plan)
        plan_save(message, plan_title=new_plan, plan_title_cor=message.text[8:])
    elif message.text[8:] not in plans[2].keys():
        plans[2].update({message.text[8:]: None})
        plan_save(message, plan_title=plans[2], plan_title_cor=message.text[8:])
    else:
        delet = await message.answer('Список дел с такой темой уже существует.\nВведите новую тему по-другому')
        await asyncio.sleep(5)
        await bot.delete_message(message.chat.id, delet.message_id)
    await bot.delete_message(message.chat.id, message.message_id)

@dp.message_handler(commands='task', state=MachineState.List)
async def plan_text(message: types.Message):
    plans = plan_save(message)

# OTHER MESSAGES

@dp.message_handler(state='*')
async def text(message: types.Message):
    dele = await message.answer(text_inline_message_warning)
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, dele.message_id)
    await bot.delete_message(message.chat.id, message.message_id)

# CALL FUNCTION IN MAIN MENU

async def next_func(callback):
    await welcome(callback)
    await correct(callback)
    await channel(callback)
    await plan(callback)

##################################################################

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    db.close()

if __name__ == '__main__':
    try:  
        executor.start_polling(dp, on_shutdown=shutdown(dp), skip_updates=True)
        asyncio.run(start)
    except asyncio.exceptions.TimeoutError: 
        pass