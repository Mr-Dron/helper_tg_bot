from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)

from app.models import Tasks

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


def create_task_keyboard(title):

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