from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
                           ReplyKeyboardMarkup, KeyboardButton)

from app.models import Companies


def choice_company_menu(companies_list: list[Companies]) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Создать",
                callback_data="create_company"
            )
        ]
    ])

    if len(companies_list) == 0:
        return keyboard
    
    for company in companies_list:
        company_button = [InlineKeyboardButton(
            text=company.name,
            callback_data=f"preview_company_{company.id}"
        )]
        keyboard.inline_keyboard.insert(0, company_button)

    return keyboard


def return_to_menu():

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Вернуться в меню",
                callback_data="return_menu"
            )
        ]
    ])

    return keyboard

def login_company_keyboard():

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Вернуться к списку компаний",
                    callback_data="my_companies"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Войти",
                    callback_data=f"login_company"
                )
            ]
        ]
    )

    return keyboard

def company_menu_keyboard():

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Задачи",
                    callback_data="company_tasks"
                ),
                InlineKeyboardButton(
                    text="сотрудники",
                    callback_data="company_employees"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Вернуться в меню",
                    callback_data="return_menu"
                )
            ]

        ]
    )

    return keyboard