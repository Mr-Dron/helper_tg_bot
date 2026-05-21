from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import menu
from app.states.echo import EchoState
from app.models import Users

router = Router()


@router.message(CommandStart())
async def start(message: Message):

    await message.answer("<b>Добро пожаловать!</b>\n" \
                        "Это бот помощник, менеджер задач. Он поможе вам не потерять задчаи, " \
                        "следить за процессом выполнения и не переживать о том что что-то будет забыто или потеряно. " \
                        "Бот напомнит о задачах на сегодня, покажет все запланированные задачи для конкретной компании или даст возможность " \
                        "создать несколько компаний и в каждой будут свои сотрудники и задачи.\n" \
                        "Компании это достаточно громкое название, ведь это могут быть и личные задачи, например сходить в магазин, убраться дома " \
                        "или выгулять собаку. Тогда компания может стать списком задач семьи, друзей или вашим личным, здесь вас ограничивает только " \
                        "ваша фантазия.\n\n" \
                        "Этот проект двигается на чистом энтузиазме и вере в светлое будущее)\n" \
                        "Version: pre-alpha 1.0.0",
                        parse_mode="HTML",
                        reply_markup=menu.main_menu()
                        )


@router.callback_query(F.data == "me")
async def me_info(callback: CallbackQuery,
                  user: Users,
                  db: AsyncSession):

    text = (
        f"ID: {user.id}\n"
        f"Имя: {user.first_name}\n"
        f"Имя пользователя: {user.username}\n" 
        f"Ссылка: {user.telegram_url}"
    )

    await callback.message.answer(
        text,
        parse_mode="HTML",
        reply_markup=menu.back_menu()
    )

    await callback.answer()


# @router.callback_query(F.data == "update_me")
# async def update_user_data()

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