from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)

from app.models import EmployeesCompany

def employees_menu_keyboard(employees_list: list[EmployeesCompany],
                           total_page: int, current_page: int):
    buttons_list = []

    for employee in employees_list:
        button = InlineKeyboardButton(
            text = f"#{employee.user_id}: {employee.employees.first_name}",
            callback_data=f"login_employee_{employee.user_id}"
        )
        buttons_list.append(button)


    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons_list,
        [
            InlineKeyboardButton(
                text="Добавить",
                callback_data="add_new_employee"
            ),
            InlineKeyboardButton(
                text="В меню",
                callback_data="company_menu"
            )
        ]
    ])

    previous_button = InlineKeyboardButton(
        text="Назад",
        callback_data="page_employees_previous"
    )
    next_button = InlineKeyboardButton(
        text="Вперед",
        callback_data="page_employees_next"
    )

    if current_page < total_page and current_page > 1:
        keyboard.inline_keyboard.insert(1, [previous_button, next_button])
    elif current_page == total_page and total_page > 1:
        keyboard.inline_keyboard.insert(1, [previous_button])
    elif current_page == 1 and total_page > 1:
        keyboard.inline_keyboard.insert(1, [next_button])
    
    return keyboard

def return_employee_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Список сотрудников",
                callback_data="company_employees"
            ),
            InlineKeyboardButton(
                text="Меню компании",
                callback_data="company_menu"
            )
        ]
    ])

    return keyboard