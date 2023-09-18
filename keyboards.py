# Keyboards

from aiogram import types
from aiogram.types.web_app_info import WebAppInfo
from DataBase import * 
# Inline keyboards for list work

def WorkKeybords(callback: types.CallbackQuery) -> types.InlineKeyboardMarkup:
    '''
    Создаёт новую клавиатуру со списком задач каждого пользователя. 
        Возвращает `types.InlineKeyboardMarkup`
    '''
    keyboard = database.plan_save(callback.message)
    markup = types.InlineKeyboardMarkup(1)
    for i in keyboard[2].keys():
        button = types.InlineKeyboardButton(i, callback_data='list_' + i)
        markup.add(button)
    markup.add(_ib7_3, _ib7)
    return markup

# Inline keyboards

_ib1 = types.InlineKeyboardButton('⬅️', callback_data='previous')
_ib2 = types.InlineKeyboardButton('➡️', callback_data='next')
_ib3 = types.InlineKeyboardButton('Хочу купить', callback_data='buy')
_ib5_1 = types.InlineKeyboardButton('Оплатить', pay=True)
_ib5_2 = types.InlineKeyboardButton('Удалить сообщение', callback_data='del')
_ib6_1 = types.InlineKeyboardButton('Показать мой список задач', callback_data='plan')
_ib7 = types.InlineKeyboardButton('Назад', callback_data='back')
_ib7_1 = types.InlineKeyboardButton('Назад', callback_data='back_worklist')
_ib7_2 = types.InlineKeyboardButton('Обновить', callback_data='update_worklist')
_ib7_3 = types.InlineKeyboardButton('Обновить', callback_data='update_plan')
_ib11 = types.InlineKeyboardButton('Ссылка на меня', url='https://t.me/p_arti_a')
_ib12 = types.InlineKeyboardButton('WEBAPP в Телеграмм', web_app=WebAppInfo(url='https://webappcontent.telegram.org/cafe?user_id=123213231&user_hash=85efe15d11be1cc64a#tgWebAppData=query_id%3DAAEj-y9hAAAAACP7L2Fc1Yms%26user%3D%257B%2522id%2522%253A1630534435%252C%2522first_name%2522%253A%2522%25D0%2590%25D1%2580%25D1%2581%25D0%25B5%25D0%25BD%2522%252C%2522last_name%2522%253A%2522%25D0%259F%25D0%25BE%25D0%25B3%25D0%25BE%25D1%2581%25D1%258C%25D1%258F%25D0%25BD%2522%252C%2522username%2522%253A%2522Arsen1963%2522%252C%2522language_code%2522%253A%2522ru%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1695049245%26hash%3Decd0009ca01552e52b99cf351ed647305948958acb2b593c15a45df406b1cebe&tgWebAppVersion=6.9&tgWebAppPlatform=web&tgWebAppBotInline=1&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22button_color%22%3A%22%233390ec%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%23707579%22%2C%22link_color%22%3A%22%2300488f%22%2C%22secondary_bg_color%22%3A%22%23f4f4f5%22%2C%22text_color%22%3A%22%23000000%22%7D'))


# Ready inline keyboards

start_keyboard = types.InlineKeyboardMarkup().add(_ib1, _ib2)
back_keyboard = types.InlineKeyboardMarkup().add(_ib7)
back_update_keyboard = types.InlineKeyboardMarkup(1).add(_ib7_3, _ib7)
back_worklist_keyboard = types.InlineKeyboardMarkup().add(_ib7_1)
back_update_worklist_keyboard = types.InlineKeyboardMarkup(1).add(_ib7_2, _ib7_1)

buy_vote = types.InlineKeyboardMarkup().add(_ib1, _ib2).add(_ib3)
about_keyboard = types.InlineKeyboardMarkup().add(_ib1, _ib2).add(_ib11)
delete_keyboard = types.InlineKeyboardMarkup(1).add(_ib5_1, _ib5_2)
plan_keyboard = types.InlineKeyboardMarkup().add(_ib1, _ib2).add(_ib6_1)
web_keyboard = types.InlineKeyboardMarkup().add(_ib1, _ib2).add(_ib12) #web_keyboard 
