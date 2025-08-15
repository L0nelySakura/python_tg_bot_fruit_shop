from aiogram import Router
from aiogram.types import Message, InputFile, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from internal.services.report import generate_sales_report_excel  # твоя функция генерации excel


router = Router()

class SalesRepStates(StatesGroup):
    waiting_for_month = State()


# Функция вызывается из common.py
async def ask_rep_month(message: Message, state: FSMContext):
    await state.set_state(SalesRepStates.waiting_for_month)
    await message.answer(
        "📆 Введите месяц и год отчёта в формате ММ.ГГГГ\n"
        "Например: 06.2025"
    )


# Обработка ввода месяца пользователем
@router.message(SalesRepStates.waiting_for_month)
async def process_month_input(message: Message, state: FSMContext):
    text = message.text.strip()
    try:
        month, year = map(int, text.split("."))
        if not (1 <= month <= 12):
            raise ValueError
    except ValueError:
        await message.answer("⛔ Неверный формат! Используйте ММ.ГГГГ")
        return

    await message.answer(f"⏳ Генерируем отчёт за {month:02}.{year}...")

    # Генерация и отправка отчёта
    try:
        file_path = await generate_sales_report_excel(month, year)
        await message.answer_document(caption="✅ Отчёт готов!",
                                      document=FSInputFile(path=file_path, filename=f"Отчёт за {month:02}_{year}.xlsx"))

    except Exception as e:
        await message.answer(f"⛔ Ошибка при генерации отчёта: {e}")

    # После отчёта FSM очищается
    await state.clear()
