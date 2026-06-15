import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import TaskStatus
from app.models import Tasks, Users
from app.repositories import (task as task_rep,
                              employee as employee_rep)
from app.helpers import task as task_help
from app.keyboards import task as task_key

async def build_task_menu_context(company_id: int, current_page: int, db: AsyncSession):

    tasks = await task_rep.get_tasks_company(company_id=company_id,
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

    return text, keyboard


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

async def current_task_menu(task_id: int, db: AsyncSession):

    task = await task_rep.get_current_task(task_id=task_id, db=db)

    text = await task_help.prepate_text_current_task_menu(task=task)

    keyborad = task_key.current_task_keyboard()

    return text, keyborad

async def edit_status_task(task_id: int, db: AsyncSession):

    task = await task_rep.get_current_task(task_id=task_id, db=db)
    text = await task_help.prepare_text_edit_status(task=task)

    keyboard = task_key.status_task_keyboard(task_id=task_id)

    return text, keyboard

async def uppend_status_task(task_id: int, new_status: str, db: AsyncSession):
    task = await task_rep.get_current_task(task_id=task_id, db=db)
    task.status = TaskStatus[new_status]

    await db.flush()

async def choose_new_responsible(current_page: int, task_id: int, 
                                 company_id: int, db: AsyncSession):

    employees_data = await employee_rep.get_employees_company_with_tasks(current_page=current_page,
                                                                    company_id=company_id,
                                                                    db=db)
    total_page = await employee_rep.get_count_employees_company(company_id=company_id,
                                                                db=db)
    
    text = await task_help.text_choose_new_responsible(employees_data=employees_data,
                                                       current_page=current_page,
                                                       total_page=total_page)
    
    employees = [row.EmployeesCompany for row in employees_data]

    keyboard = task_key.choose_new_responsible(total_page=total_page,
                                               current_page=current_page,
                                               task_id=task_id,
                                               employees=employees)

    return text, keyboard
