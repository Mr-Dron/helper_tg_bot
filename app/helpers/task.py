import math

from aiogram import html

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Row

from app.models import Tasks, EmployeesCompany, Users
from app.repositories import task as task_per

async def prepare_text_tasks_menu(tasks_list: list[Tasks], current_page: int, total_page: int):

    text = ""

    if not tasks_list:
        text += "Нет активных задач\n"
    else:
        for task in tasks_list:
            text += f"{task.status.value} #{task.id} {task.title}\n"

    text += f"\nСтраница {current_page} из {total_page}"

    return text

async def count_pages(company_id: int, db: AsyncSession):

    total_tasks = await task_per.get_count_tasks_company(company_id=company_id,\
                                                         db=db)

    total_pages = math.ceil(total_tasks / 4)

    if total_pages == 0:
        total_pages += 1

    return total_pages

async def prepare_text_task_create(responsible_id: int, title: str, description: str):

    fields = {
        "Название": title,
        "Описание": description,
        "Ответственный": responsible_id
    }

    lines = [
        f"{label}: {value if value else '_Не заполнено_'}"
        for label, value in fields.items()
    ]

    return f"*Карточка новой задачи*\n\n" + "\n".join(lines)

async def prepate_text_save_task(task: Tasks):

    text = "Задача сохранена\n"\
           f"Номер: #{task.id}\n"\
           f"Название: {task.title}\n"\
           f"Описание: {task.description}\n"\
           f"Создатель: {task.creator_id}\n"\
           f"Ответственный: {task.responsible_id}\n"\
           f"Компания: {task.company_id}"
    
    return text

async def prepate_text_current_task_menu(task: Tasks):

    fields = {
        "Название": task.title,
        "Описание": task.description,
        "Ответственный": formatter_worker_link(task.responsible),
        "Создатель": formatter_worker_link(task.creator),
        "Этап": task.status.value,
        "Компаний": task.company_id
    }

    lines = [
        f"{label}: {value if value and value != "@" else '_Не заполнено_'}"
        for label, value in fields.items()
    ]

    return "*Карточка задачи*\n\n" + "\n".join(lines)

async def prepare_text_edit_status(task: Tasks):
    fields = {
        "Название": task.title,
        "Описание": task.description,
        "Ответственный": formatter_worker_link(task.responsible),
    }

    lines = [
        f"{label}: {value if value and value != "@" else '_Не заполнено_'}"
        for label, value in fields.items()
    ]

    return f"*Текущий этап: {task.status.value}*\n\n" + "\n".join(lines)

async def text_choose_new_responsible(employees_data: list[Row],
                                      current_page: int, total_page: int):
    
    lines = []
    
    for employee, user, task_count in employees_data:
        if not task_count:
            task_count = 0
        lines.append(f"#{employee.id} "\
                     f"{user.first_name} _должность_\n"\
                     f"Активных задач ({task_count})")

    return "Выберите ответсвенного\n"\
           f"Страница {current_page} из {total_page}\n\n" + "\n".join(lines)

def formatter_worker_link(user: Users):

    if user.username:
        clean_username = user.username.lstrip("@")
        return html.link(value=user.first_name, link=f"tg://resolve?domain={clean_username}")
    elif user.telegram_id:
        return html.link(value=user.first_name, link=f"tg://user?id={user.telegram_id}")