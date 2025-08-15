from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from internal.handlers.director import ask_director_password
from internal.keyboards.common_kb import get_main_menu
from internal.handlers.sales_rep import ask_rep_month

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    kb = get_main_menu()
    await message.answer("""
👋 <b>Добро пожаловать!</b>
Выберите одну из команд:
👔 <b>Директор</b> - ввод продаж.
🛒 <b>Торговый представитель</b> - вывод плана продаж.
Нажмите на кнопку ниже, чтобы начать.
""",
                         reply_markup=kb,
                         parse_mode="HTML")


@router.callback_query(lambda c: c.data == "director")
async def director_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await ask_director_password(callback.message, state)


@router.callback_query(lambda c: c.data == "representative")
async def rep_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await ask_rep_month(callback.message, state)
