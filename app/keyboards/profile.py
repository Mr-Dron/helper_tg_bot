from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def update_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Изменить имя",
                    callback_data="update_name"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Изменить имя пользователя",
                    callback_data="update_username"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Изменить ссылку",
                    callback_data="update_url"
                )
            ]
        ]
    )

def take_data_update_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Взять автоматически из профиля",
                    callback_data="take_auto"
                )
            ]
        ]
    )