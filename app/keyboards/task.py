from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)

from app.models import Tasks, EmployeesCompany
from app.core.database import TaskStatus

def tasks_menu(tasks_list: list[Tasks], total_page: int, current_page: int):
    
    buttons = []

    for task in tasks_list:
        buttons.append(
            InlineKeyboardButton(
                text=f"#{task.id}",
                callback_data=f"login_task_{task.id}"
            )
        )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [
            InlineKeyboardButton(
                text="Создать задачу",
                callback_data="create_task",
            ),
            InlineKeyboardButton(
                text="В меню",
                callback_data="company_menu"
            )
        ]
    ])

    previous_button = InlineKeyboardButton(
        text="Назад",
        callback_data="page_tasks_previous"
    )
    next_button = InlineKeyboardButton(
        text="Вперед",
        callback_data="page_tasks_next"
    )

    if current_page == 1 and total_page > 1:
        keyboard.inline_keyboard.insert(1, [next_button])
    elif current_page > 1 and current_page < total_page:
        keyboard.inline_keyboard.insert(1, [previous_button, next_button])
    elif current_page > 1 and current_page == total_page:
        keyboard.inline_keyboard.insert(1, [previous_button])

    return keyboard


def create_task_keyboard(title: str):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Изменить название",
                    callback_data="edit_title"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Изменить описание",
                    callback_data="edit_description"
                )
            ],
            # [
            #     InlineKeyboardButton(
            #         text="Изменить ответственного",
            #         callback_data="edit_responsible"
            #     )
            # ]
        ]
    )

    cancel_button = InlineKeyboardButton(
        text="Отмена",
        callback_data="cancel_task_create"
    )
    active_save_button = InlineKeyboardButton(
        text="Сохранить задачу",
        callback_data="save_new_task"
    )
    inactive_save_button = InlineKeyboardButton(
        text="Заполните данные",
        callback_data="inactive_save_task"
    )

    if not title:
        keyboard.inline_keyboard.append([cancel_button, inactive_save_button])
    else:
        keyboard.inline_keyboard.append([cancel_button, active_save_button])
    
    return keyboard

def save_task_keyboard():

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Вернуться к списку задач",
                callback_data="company_tasks"
            ),
            InlineKeyboardButton(
                text="Веруться в меню компании",
                callback_data="company_menu"
            )
        ],
        [
            InlineKeyboardButton(
                text="Изменить задачу",
                callback_data="edit_task"
            )
        ]
    ])

    return keyboard

def current_task_keyboard():

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Сменить статус",
                callback_data="task_new_status"
            ),
            InlineKeyboardButton(
                text="Назначить",
                callback_data="task_new_responsible"
            )
        ],
        [
            InlineKeyboardButton(
                text="Редактировать",
                callback_data="3"
            )
        ],
        [
            InlineKeyboardButton(
                text="Меню компании",
                callback_data="company_menu"
            ),
            InlineKeyboardButton(
                text="Список задач",
                callback_data="company_tasks"
            )
        ]
    ])

    return keyboard

def status_task_keyboard(task_id: int):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data=f"login_task_{task_id}"
            )
        ]
    ])

    for status in TaskStatus:
        button = InlineKeyboardButton(
            text=status.value,
            callback_data=status.name
        )
        keyboard.inline_keyboard.append([button])
    
    return keyboard

def choose_new_responsible(total_page: int, current_page: int, task_id: int,
                           employees: list[EmployeesCompany]):
    
    employees_buttons = []

    for employee in employees:
        button = InlineKeyboardButton(
            text = f"#{employee.id}",
            callback_data=f"new_responsible_{employee.user_id}"
        )
        employees_buttons.append(button)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        employees_buttons,
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data=f"login_task_{task_id}"
            )
        ]
    ])

    previuos_button = InlineKeyboardButton(
        text="Предыдущая",
        callback_data="previuos_page_new_responsible"
    )
    next_button = InlineKeyboardButton(
        text="Следующая",
        callback_data="next_page_new_responsible"
    )

    if current_page > 1 and total_page > current_page:
        keyboard.inline_keyboard.insert(1, [previuos_button, next_button])
    elif total_page == current_page and total_page > 1:
        keyboard.inline_keyboard.insert(1, [previuos_button])
    elif current_page == 1 and total_page > 1:
        keyboard.inline_keyboard.insert(1, [next_button])
    
    return keyboard