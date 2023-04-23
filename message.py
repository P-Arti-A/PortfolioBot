import asyncio

from aiogram import Dispatcher, types

from DataBase import database
from init import *
from textpad import *
from keyboards import *
from MachineState import MachineState

class Messages:
    def __init__(self, id) -> None:
        self.id = id
        self.send_message = bot.send_message
        self.delete_message = bot.delete_message
        self.database = database

    # def return_database(self, plan_save:bool = False, message):
    #     if plan_save:
    #         return db.plan_save(message)
    #     else:
    #         return db.data_save(message)

    # START

    async def start(message: types.Message):
        user = database.data_save(message)
        if user[-1] is not None:
            try:
                await bot.delete_message(message.chat.id, user[-1])
            except:
                pass
        await bot.delete_message(message.chat.id, message.message_id)
        message_id = await bot.send_message(message.chat.id, text_inline_start, reply_markup=start_keyboard)
        user(message, message_id.message_id)

    # CREATE WORK PLANS

    async def plan_text(message: types.Message):
        plans = database.plan_save(message)
        new_plan = plans[2].get(message.text[8:], None)
        if plans[2] is None:
            new_plan = {message.text[8:]: None}
            print(new_plan)
            database.plan_save(message, plan_title=new_plan, plan_title_cor=message.text[8:])
        elif message.text[8:] not in plans[2].keys():
            plans[2].update({message.text[8:]: None})
            database.plan_save(message, plan_title=plans[2], plan_title_cor=message.text[8:])
        else:
            delet = await message.answer('Список дел с такой темой уже существует.\nВведите новую тему по-другому')
            await asyncio.sleep(5)
            await bot.delete_message(message.chat.id, delet.message_id)
        await bot.delete_message(message.chat.id, message.message_id)

    async def task(message: types.Message):
        plans = database.plan_save(message)

    # OTHER MESSAGES

    async def text(message: types.Message):
        dele = await message.answer(text_inline_message_warning)
        await asyncio.sleep(5)
        await bot.delete_message(message.chat.id, dele.message_id)
        await bot.delete_message(message.chat.id, message.message_id)

#############################################################################################

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(Messages.start, commands='start', state='*')
    dp.register_message_handler(Messages.plan_text, commands='create', state=MachineState.List)
    dp.register_message_handler(Messages.task, commands='task', state=MachineState.List)
    dp.register_message_handler(Messages.text, state='*') 