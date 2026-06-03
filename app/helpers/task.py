import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tasks
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

    text = "Создание новой задач\n"

    if not title:
        text += "Название: Не заполнено\n"
    else:
        text += f"Название: {title}\n"
    
    if not description:
        text += "Описание: Не заполнено\n"
    else:
        text += f"Описание: {description}\n"
    
    if not responsible_id:
        text += "Ответственный: Не назначен\n"
    else:
        text += f"Ответственный: {responsible_id}\n"

    return text

async def prepate_text_save_task(task: Tasks):

    text = "Задача сохранена\n"\
           f"Номер: #{task.id}\n"\
           f"Название: {task.title}\n"\
           f"Описание: {task.description}\n"\
           f"Создатель: {task.creator_id}\n"\
           f"Ответственный: {task.responsible_id}\n"\
           f"Компания: {task.company_id}"
    
    return text