import asyncio

from aiogram import Dispatcher, types

from DataBase import database
from init import *
from textpad import *
from keyboards import *
from MachineState import MachineState, MachineState_1

async def start(message: types.Message):
    try:
        n = dp.storage.data[str(message.chat.id)][str(message.chat.id)]
        if n['state'] is not None:
            await MachineState.first()
    except KeyError:
        await MachineState.first()
    user = database.data_save(message)
    if user[-1] is not None:
        try:
            await bot.delete_message(message.chat.id, user[-1])
        except:
            pass
    await bot.delete_message(message.chat.id, message.message_id)
    message_id = await bot.send_message(message.chat.id, text_inline_start, reply_markup=start_keyboard)
    database.data_save(message, message_id.message_id)

# CREATE WORK PLANS

async def plan_text(message: types.Message):
    plans = database.plan_save(message)
    if plans is None:
        new_plan = {message.text[8:]: None}
        database.plan_save(message, plan_title=new_plan, plan_title_cor=message.text[8:])
        delet = await message.answer('Список задач ' + message.text[8:] + ' создан!')
    elif message.text[8:].isspace() or len(message.text[8:]) == 0:
        delet = await message.answer('После "/create" укажите название нового списка задач!')
    elif message.text[8:] not in plans[2].keys():
        new_plan = plans[2]
        new_plan.update({message.text[8:]: None})
        database.plan_save(message, plan_title=new_plan, plan_title_cor=message.text[8:])
        delet = await message.answer('Список задач ' + message.text[8:] + ' создан!')
    else:
        delet = await message.answer('Список задач с такой темой уже существует.\nВведите новую тему по-другому')
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, delet.message_id)
    await bot.delete_message(message.chat.id, message.message_id)

# CREATE WORK PLANS

async def plan_del(message: types.Message):
    plans = database.plan_save(message)
    if plans is None:
        delet = await message.answer('Список задач ' + message.text[8:] + ' создан!')
        await asyncio.sleep(5)
        await bot.delete_message(message.chat.id, delet.message_id)
    elif message.text[8:].isspace() or len(message.text[8:]) == 0:
        delet = await message.answer('После "/delete" укажите название списка задач, который нужно удалить!')
        await asyncio.sleep(5)
        await bot.delete_message(message.chat.id, delet.message_id)
    elif message.text[8:] in plans[2].keys():
        new_plan = plans[2]
        del new_plan[message.text[8:]]
        database.plan_save(message, plan_title=new_plan)
        delet = await message.answer('Список задач ' + message.text[8:] + ' удалён!')
        await asyncio.sleep(5)
        await bot.delete_message(message.chat.id, delet.message_id)
    else:
        delet = await message.answer('Список задач с такой темой не существует.\nВведите существующий список задач для его удаления')
        await asyncio.sleep(5)
        await bot.delete_message(message.chat.id, delet.message_id)
    await bot.delete_message(message.chat.id, message.message_id)
        
# CREATE|DELETE PLANS IN LIST

async def task(message: types.Message):
    plans = database.plan_save(message)
    if plans[2][plans[3]] is None:
        plans[2][plans[3]] = [message.text]
        dele = await message.answer('Добавил новая задача!\n\n' + message.text + '\n\nНажмите "Обновить", чтобы увидеть новую задачу в вашем списке.')
    else:
        try:
            text = plans[2][plans[3]].pop(int(message.text)-1)
            if len(plans[2][plans[3]]) == 0:
                plans[2][plans[3]] = None
            dele = await message.answer('Задача: "' + text + '" была удалена.')
        except IndexError:
            dele = await message.answer('Номер задачи: "' + message.text + '" не существует!\nОтправьте номер задачи, которую хотите удалить, либо напишите название новой задачи.')
        except (TypeError, ValueError):
            plans[2][plans[3]].append(message.text)
            dele = await message.answer('Добавил новая задача!\n\n' + message.text + '\n\nНажмите "Обновить", чтобы увидеть новую задачу в вашем списке.')
    database.plan_save(message, plan_title=plans[2])
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, dele.message_id)
    await bot.delete_message(message.chat.id, message.message_id)

async def warning(message: types.Message):
    dele = await message.answer(text_plan_warning)
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, dele.message_id)
    await bot.delete_message(message.chat.id, message.message_id)

# OTHER MESSAGES

async def text(message: types.Message):
    dele = await message.answer(text_inline_message_warning)
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, dele.message_id)
    await bot.delete_message(message.chat.id, message.message_id)

#############################################################################################

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(plan_text, commands='create', state=MachineState_1.List_main)
    dp.register_message_handler(plan_del, commands='delete', state=MachineState_1.List_main)
    dp.register_message_handler(warning, state=MachineState.List)
    dp.register_message_handler(task, state=MachineState_1.List_create)
    dp.register_message_handler(text, state='*') 