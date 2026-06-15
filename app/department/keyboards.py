from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from app.models import EmployeesCompany, Departments

def create_menu(dep_name: str):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Название",
                callback_data="edit_name_new_dep"
            )
        ],
        [
            InlineKeyboardButton(
                text="Ответственный",
                callback_data="new_resp_new_dep"
            )
        ]
    ])

    cancel_button = InlineKeyboardButton(
        text="Отменить",
        callback_data="company_menu"
    )

    inactive_save_button = InlineKeyboardButton(
        text="Неактивна",
        callback_data="inactive_save_new_dep"
    )

    active_save_button = InlineKeyboardButton(
        text="Сохранить",
        callback_data="active_save_new_dep"
    )

    if not dep_name:
        keyboard.inline_keyboard.append([cancel_button, inactive_save_button])
    else:
        keyboard.inline_keyboard.append([cancel_button, active_save_button])
    
    return keyboard

def select_new_resp(total_page: int, current_page: int, employees: list[EmployeesCompany]):

    buttons = [
        InlineKeyboardButton(text=f"{employee.employees.first_name}", 
                             callback_data=f"select_new_resp_{employee.employees.id}")
        for employee in employees
    ]


    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data="create_dep"
            )
        ]
    ])

    previous_button = InlineKeyboardButton(
        text="Назад",
        callback_data="previous_page_resp_new_dep"
    )
    next_button = InlineKeyboardButton(
        text="Вперед",
        callback_data="next_page_resp_new_dep"
    )

    if current_page == 1 and total_page > 1:
        keyboard.inline_keyboard.insert(1, [next_button])
    elif current_page > 1 and total_page > current_page:
        keyboard.inline_keyboard.insert(1, [previous_button, next_button])
    elif current_page == total_page and current_page > 1:
        keyboard.inline_keyboard.insert(1, [previous_button])
    
    return keyboard


def new_card_dep():

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Войти",
                callback_data=f"login_dep"
            )
        ],
        [
            InlineKeyboardButton(
                text="Отделы",
                callback_data="company_departments"
            ),
            InlineKeyboardButton(
                text="Меню компании",
                callback_data="company_menu"
            )
        ],
        [
            InlineKeyboardButton(
                text="Изменить отдел",
                callback_data="edit_dep"
            )
        ]
    ])

    return keyboard

def all_deps_menu(current_page: int, total_page: int, deps: list[Departments]):

    buttons = [
        InlineKeyboardButton(
            text=dep.name,
            callback_data=f"login_dep_{dep.id}"
        ) for dep in deps
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [
            InlineKeyboardButton(
                text="Создать",
                callback_data="create_dep"
            ),
            InlineKeyboardButton(
                text="Меню",
                callback_data="company_menu"
            )
        ]
    ])

    previous_button = InlineKeyboardButton(
        text = "< Назад",
        callback_data="previous_page_all_deps"
    )
    next_button = InlineKeyboardButton(
        text="Вперед >",
        callback_data="next_page_all_deps"
    )

    if current_page == 1 and total_page > 1:
        keyboard.inline_keyboard.insert(1, [next_button])
    elif current_page > 1 and total_page > current_page:
        keyboard.inline_keyboard.insert(1, [previous_button, next_button])
    elif current_page > 1 and total_page == current_page:
        keyboard.inline_keyboard.insert(1, [previous_button])

    return keyboard

def dep_card():

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Задачи",
                callback_data="dep_tasks"
            ),
            InlineKeyboardButton(
                text="Сотрудники",
                callback_data="dep_members"
            )
        ],
        [
            InlineKeyboardButton(
                text="Изменить отдел",
                callback_data="edit_dep"
            )
        ],
        [
            InlineKeyboardButton(
                text="Меню",
                callback_data="return_menu"
            ),
            InlineKeyboardButton(
                text="Меню компании",
                callback_data="company_menu"
            )
        ]
    ])

    return keyboard