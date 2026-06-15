from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users, Departments, DepartmentMembers
from app.department import helpers, keyboards, schemas, repositories
from app.repositories import (employee as employee_rep, 
                              company as company_rep)

async def create_dep_menu(fields: dict, name: str = None):
    
    text = await helpers.text_create_department_menu(fields=fields)

    keyboard = keyboards.create_menu(name)

    return text, keyboard

async def select_resp_from_employees(current_page: int, company_id: int, db: AsyncSession):

    employees = await employee_rep.get_employee_company(current_page=current_page,
                                              company_id=company_id,
                                              db=db)
    
    total_page = await helpers.count_page_employees(company_id=company_id,
                                                    db=db)
    
    keyboard = keyboards.select_new_resp(total_page=total_page, current_page=current_page,
                                         employees=employees)
    
    text = await helpers.select_new_resp(employees=employees, current_page=current_page,
                                         total_page=total_page)
    
    return text, keyboard

async def save_new_dep(data: schemas.DepartmentCreate, db: AsyncSession):
    
    new_dep = await repositories.create_dep(data=data, db=db)

    if not await repositories.check_to_exists_member(member_id=data.responsible_id, 
                                           dep_id=new_dep.id, db=db):
        await repositories.add_new_member(member_id=data.responsible_id, 
                                          dep_id=new_dep.id, db=db)
    
    if not await repositories.check_to_exists_member(member_id=data.creator.id,
                                                     dep_id=new_dep.id, db=db):
        await repositories.add_new_member(member_id=data.creator.id, 
                                          dep_id=new_dep.id, db=db)
    
    data_dep = await repositories.get_current_dep(dep_id=new_dep.id,
                                                  db=db)
    
    text = await helpers.text_card_dep(data_dep=data_dep)

    keyboard = keyboards.new_card_dep()

    return text, keyboard, new_dep.id

async def total_deps_menu(current_page: int, company_id: int, db: AsyncSession):

    total_count_deps = await repositories.total_count_deps_company(company_id=company_id,
                                                                   db=db)
    total_page = await helpers.total_page_deps(total_count=total_count_deps)

    deps = await repositories.get_company_deps(current_page=current_page,
                                               company_id=company_id,
                                               db=db)
    
    text = await helpers.all_deps_menu(current_page=current_page,
                                       total_page=total_page,
                                       deps=deps)
    
    keyboard = keyboards.all_deps_menu(current_page=current_page,
                                       total_page=total_page,
                                       deps=deps)

    return text, keyboard

async def login_dep(dep_id: int, db: AsyncSession):

    dep = await repositories.get_current_dep(dep_id=dep_id,
                                             db=db)

    text = await helpers.text_card_dep(data_dep=dep,
                                       mode="view")
    
    keyboard = keyboards.dep_card()

    return text, keyboard