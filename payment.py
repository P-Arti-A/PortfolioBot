from aiogram import types
import asyncio

from textpad import *
from config import PAYMENT
from init import *
from keyboards import *
from MachineState import MachineState

Price1 = types.LabeledPrice('Подписка!', 10000)
Price2 = types.LabeledPrice('А вообще', 10000)
Price3 = types.LabeledPrice('Здесь может быть написано что угодно', 10000)

# DETAILS AND BUY PASS 

async def correct(callback:types.CallbackQuery):
    n = dp.storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]
    if n['state'] == 'MachineState:Payment':
        if callback.data == 'buy':
            await bot.send_invoice(callback.message.chat.id, 
                title=text_invoice_title, 
                description=text_invoice_description,
                provider_token=PAYMENT,
                currency='rub',
                prices=[Price1, Price2, Price3],
                payload='test_payload',
                start_parameter='subscribe',
                photo_url = 'https://i.ytimg.com/vi/Q0xMZmL8zT8/hqdefault.jpg',
                photo_size=320,
                photo_height= 360,
                photo_width=480,
                max_tip_amount=100000,
                suggested_tip_amounts=[100, 1000, 10000, 100000],
                need_phone_number=True,
                reply_markup=delete_keyboard)
        elif callback.data == 'other':
            await callback.message.edit_text(text_callback_other, reply_markup=buy_vote)
        else:

            await callback.message.edit_text(text_inline_payment, reply_markup=buy_vote)
        await callback.answer()

# Handlers pre checkout payment

async def pre_checkout_query(checkout: types.ShippingQuery):
    await bot.answer_pre_checkout_query(checkout.id, True)

# Handlers SUCCESSFUL PAYMENT

@dp.message_handler(content_types=types.message.ContentType.SUCCESSFUL_PAYMENT, state='*')
async def successful_pay(message: types.Message):
    pay_info = message.successful_payment.to_python()
    for k, v in pay_info.items():
        print(k, v, sep=' ')
    currency = pay_info.items()['currency']
    total_amount = pay_info.items()['total_amount']
    invoice_payload = pay_info.items()['invoice_payload']
    delet = await message.answer(f'''
        Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} от [{message.chat.first_name}](t.me/{message.from_user.username}), прошел успешно 
        Вы так же можете получить всю инеобходимую информацию о платеже в удобном для вас виде:
        Валюта оплаты - {currency}
        Сумма оплаты - {total_amount}
        Описание выбранного товара - {invoice_payload}
        (Сообщение удалиться через 30 секунд)''',
                        parse_mode='Markdown', 
                        disable_web_page_preview=True)
    await asyncio.sleep(30)
    await bot.delete_message(message.chat.id, delet.message_id)

def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(correct, text=['buy', 'other'], state=MachineState.Payment)
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True, state='*')
    dp.register_message_handler(successful_pay, content_types=types.message.ContentType.SUCCESSFUL_PAYMENT, state='*')