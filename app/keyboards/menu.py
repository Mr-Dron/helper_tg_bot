from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Моя информация",
                    callback_data="me"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Обновить данные",
                    callback_data="update_me"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Мои компании",
                    callback_data="my_companies"
                )
            ]
        ]
    )


def back_menu():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                text="Вернуться в меню"
                )
            ]
        ],
        resize_keyboard=True
    )