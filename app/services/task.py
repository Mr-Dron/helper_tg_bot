import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tasks, Users
from app.repositories import task as task_per
from app.helpers import task as task_help
from app.keyboards import task as task_key

async def build_task_menu_context(company_id: int, current_page: int, db: AsyncSession):

    tasks = await task_per.get_tasks_company(company_id=company_id,
                                             page=current_page,
                                             db=db)
    
    total_page = await task_help.count_pages(company_id=company_id,
                                             db=db)
    
    text = await task_help.prepare_text_tasks_menu(tasks_list=tasks,
                                                   current_page=current_page,
                                                   total_page=total_page)
    
    keyboard = task_key.tasks_menu(tasks_list=tasks,
                                   total_page=total_page,
                                   current_page=current_page)
    
    return (text, keyboard)

async def build_task_create_context(responsible_id: int=None, title:  str=None, description: str=None):
    
    text = await task_help.prepare_text_task_create(responsible_id=responsible_id,
                                                    title=title,
                                                    description=description)

    keyboard = task_key.create_task_keyboard(title)

    return (text, keyboard)


async def save_new_task(company_id: int, user: Users, title, description, db: AsyncSession):

    new_task = Tasks(title=title,
                     description=description,
                     creator_id=user.id,
                     responsible_id=user.id,
                     company_id=company_id)

    db.add(new_task)
    await db.flush()

    text = await task_help.prepate_text_save_task(new_task)
    keyboard = task_key.save_task_keyboard()

    return (text, keyboard)
