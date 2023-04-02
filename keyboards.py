# Keyboards

from aiogram import types

# Inline keyboards

_ib1 = types.InlineKeyboardButton('⬅️', callback_data='previous')
_ib2 = types.InlineKeyboardButton('➡️', callback_data='next')
_ib3 = types.InlineKeyboardButton('Хочу купить', callback_data='buy')
_ib4 = types.InlineKeyboardButton('Хочу купить что-то другое', callback_data='other')
_ib5_1 = types.InlineKeyboardButton('Оплатить', pay=True)
_ib5_2 = types.InlineKeyboardButton('Удалить сообщение', callback_data='del')
_ib6_1 = types.InlineKeyboardButton('Показать мой список дел', callback_data='plan')
_ib7 = types.InlineKeyboardButton('Назад', callback_data='back')
_ib11 = types.InlineKeyboardButton('О канале', callback_data='channel')

# Ready inline keyboards

start_keyboard = types.InlineKeyboardMarkup().add(_ib1, _ib2)
back_keyboard = types.InlineKeyboardMarkup().add(_ib7)

buy_vote = types.InlineKeyboardMarkup().add(_ib1, _ib2).add(_ib3).add(_ib4)
about_keyboard = types.InlineKeyboardMarkup().add(_ib1, _ib2).add(_ib11)
delete_keyboard = types.InlineKeyboardMarkup(1).add(_ib5_1, _ib5_2)
plan_keyboard = types.InlineKeyboardMarkup().add(_ib1, _ib2).add(_ib6_1)