from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from app.services import profile as profile_ser
from app.keyboards import menu, profile as profile_key
from app.models import Users
from app.states.profile import UpdateProfileState

router = Router()

@router.callback_query(F.data == "me")
async def me_info(callback: CallbackQuery,
                  user: Users,
                  db: AsyncSession):

    text = f"ID: {user.id}\n" + await profile_ser.build_profile_text(user)

    await callback.message.answer(
        text,
        parse_mode="HTML",
        reply_markup=menu.back_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "update_me")
async def update_profile(callback: CallbackQuery,
                         user: Users,
                         db: AsyncSession):
    
    await profile_ser.send_update_profile_menu(
        callback.message,
        user)
    
    await callback.answer()

@router.callback_query(F.data == "update_name")
async def update_first_name(callback: CallbackQuery,
                            user: Users,
                            state: FSMContext):
    
    text = (f"Текущее имя: {user.first_name}\n"
            "Введите новое имя...")
    
    await state.set_state(UpdateProfileState.waiting_for_firstname)

    await callback.message.answer(
        text,
        reply_markup=profile_key.take_data_update_menu()
    )

    await callback.answer()

@router.callback_query(
        UpdateProfileState.waiting_for_firstname,
        F.data == "take_auto"
)
async def read_auto_update_first_name(callback: CallbackQuery,
                                      user: Users,
                                      db: AsyncSession,
                                      state: FSMContext):
    
    user.first_name = callback.from_user.first_name

    await db.flush()

    await state.clear()
    
    await callback.message.answer("Имя обнавлено")

    await profile_ser.send_update_profile_menu(callback.message,
                                               user)

@router.message(
        UpdateProfileState.waiting_for_firstname
)   
async def read_updated_first_name(message: Message,
                                  user: Users,
                                  state: FSMContext,
                                  db: AsyncSession):
    user.first_name = message.text

    await db.flush()

    await state.clear()
    
    await message.answer("Имя обнавлено")

    await profile_ser.send_update_profile_menu(message,
                                               user)


@router.callback_query(F.data == "update_username")
async def update_username(callback: CallbackQuery,
                          state: FSMContext,
                          user: Users):
    text = (f"Текущее имя пользователя: {user.username}\n")
    
    await state.set_state(UpdateProfileState.waiting_for_username)

    await callback.message.answer(
        text,
        reply_markup=profile_key.take_data_update_menu()
    )

    await callback.answer()

@router.callback_query(
        UpdateProfileState.waiting_for_username,
        F.data == "take_auto")
async def read_auto_update_username(callback: CallbackQuery,
                                    state: FSMContext,
                                    user: Users,
                                    db: AsyncSession):
    
    user.username = callback.from_user.username

    await db.flush()

    await state.clear()

    await profile_ser.send_update_profile_menu(callback.message, user)

@router.callback_query(F.data == "update_url")
async def update_telegram_url(callback: CallbackQuery,
                              state: FSMContext,
                              user: Users):
    
    text = (f"Текущее ссылка: {user.telegram_url}\n")
    
    await state.set_state(UpdateProfileState.waiting_for_telegramlink)

    await callback.message.answer(
        text,
        reply_markup=profile_key.take_data_update_menu()
    )

    await callback.answer()

@router.callback_query(
        UpdateProfileState.waiting_for_telegramlink,
        F.data == "take_auto")
async def read_auto_update_username(callback: CallbackQuery,
                                    state: FSMContext,
                                    user: Users,
                                    db: AsyncSession):
    
    username = callback.from_user.username

    user.telegram_url = f"https://t.me/{username}"

    await db.flush()

    await state.clear()

    await profile_ser.send_update_profile_menu(callback.message, user)