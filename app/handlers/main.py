from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import decode_payload

from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import menu
from app.states.echo import EchoState
from app.models import Users
from app.repositories import employee as employee_rep

router = Router()


@router.message(CommandStart())
async def start(message: Message,
                command: CommandObject,
                state: FSMContext,
                db: AsyncSession):

    await state.clear()

    args = command.args

    if args:

        payload = decode_payload(args)
        if payload.startswith("inv_"):
            token = payload.replace("inv_", "")

            invite = await employee_rep.check_invite_token(token=token,
                                                        db=db)
            
            if not token:
                await message.answer(text="Эта ссылку уже старела или не существует",
                                     reply_markup=menu.main_menu())
                return
                
            
            is_exists = await employee_rep.check_exists_employee(invite.company_id,
                                                        message.from_user.id,
                                                        db=db)
            
            if is_exists:
                await message.answer(text="Вы уже являетесь сотрудником этой компании!",
                                     reply_markup=menu.main_menu())
                return

            await employee_rep.add_new_employee(comapny_id=invite.company_id,
                                                telegram_id=message.from_user.id,
                                                db=db)
            
            await message.answer(
                text="Добро пожаловать!\nВы успешно добавлены в компанию и теперь можете видеть активные задачи",
                reply_markup=menu.main_menu())

            return

    await message.answer("<b>Добро пожаловать!</b>\n" \
                        "Это бот помощник, менеджер задач. Он поможе вам не потерять задчаи, " \
                        "следить за процессом выполнения и не переживать о том что что-то будет забыто или потеряно. " \
                        "Бот напомнит о задачах на сегодня, покажет все запланированные задачи для конкретной компании или даст возможность " \
                        "создать несколько компаний и в каждой будут свои сотрудники и задачи.\n" \
                        "Компании это достаточно громкое название, ведь это могут быть и личные задачи, например сходить в магазин, убраться дома " \
                        "или выгулять собаку. Тогда компания может стать списком задач семьи, друзей или вашим личным, здесь вас ограничивает только " \
                        "ваша фантазия.\n\n" \
                        "Этот проект двигается на чистом энтузиазме и вере в светлое будущее)\n" \
                        "Version: Alpha 1.0.1",
                        parse_mode="HTML",
                        reply_markup=menu.main_menu()
                        )



@router.callback_query(F.data == "echo")
async def echo_mode(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.set_state(EchoState.active)

    await callback.message.answer(
        "Эхо режим включен",
        reply_markup=menu.back_menu()
    )

    await callback.answer()


@router.message(
    EchoState.active,
    F.text != "Вернуться в меню"
)
async def echo_handler(message: Message):
    
    await message.answer(message.text)


@router.message(
    F.text == "Вернуться в меню"
)
async def back_to_menu(message: Message,
                       state: FSMContext):
    
    await state.clear()

    await message.answer(
        "Главное меню",
        reply_markup=menu.main_menu()
    )

@router.callback_query(
    F.data == "return_menu",
    StateFilter("*")
)
async def back_to_menu_callback(callback: CallbackQuery,
                       state: FSMContext):
    
    await state.clear()

    await callback.message.answer(
        "Главное меню",
        reply_markup=menu.main_menu()
    )