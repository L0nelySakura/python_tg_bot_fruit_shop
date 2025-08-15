from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from internal.config.config import STORE_PASSWORDS, STORE_INFO
from internal.services.gsheet import append_sales_row
from internal.keyboards.common_kb import get_main_menu
from datetime import datetime

router = Router()


class DirectorStates(StatesGroup):
    waiting_for_password = State()
    waiting_for_date = State()
    waiting_for_sales = State()


async def ask_director_password(message: Message, state: FSMContext):
    data = await state.get_data()
    if "store_id" in data:
        await message.answer("✅ Вы уже вошли как директор.\n"
                             "Введите дату продаж в формате ДД.MM.ГГГГ:\n"
                             "Для выхода из аккаунта нажмите /logout")
        await state.set_state(DirectorStates.waiting_for_date)
        return

    await state.set_state(DirectorStates.waiting_for_password)
    await message.answer("🔒 Введите код доступа:")


# Logout
@router.message(Command("logout"))
async def logout(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🚪 Вы вышли из аккаунта.")

    kb = get_main_menu()
    await message.answer("""
👋 <b>Добро пожаловать!</b>
Выберите одну из команд:
👔 <b>Директор</b> - вводите продажи и управляете магазином.
🛒 <b>Торговый представитель</b> -.
Нажмите на кнопку ниже, чтобы начать.
    """,
                         reply_markup=kb,
                         parse_mode="HTML")


# Проверка пароля
@router.message(DirectorStates.waiting_for_password)
async def check_director_password(message: Message, state: FSMContext):
    password = message.text.strip()
    if password in STORE_PASSWORDS:

        store_id = STORE_PASSWORDS[password]
        store_data = STORE_INFO.get(store_id, {})

        print(f"[INFO] Новый вход в магазин с id {store_id} от telegram id: {message.from_user.id}.")

        await state.update_data(store_id=store_id)
        await message.answer(f"""✅ Доступ разрешён

🏬 Магазин: {store_data.get('name', 'Неизвестно')} (ID: {store_id})
📊 Планы по фруктам за месяц:
    🍐 Груши: {store_data.get('pears_plan', 0)}
    🍎 Яблоки: {store_data.get('apples_plan', 0)}
    🍊 Апельсины: {store_data.get('oranges_plan', 0)}
    🍊 Мандарины: {store_data.get('mandarins_plan', 0)}
    🍍 Ананасы: {store_data.get('pineapples_plan', 0)}""")
        await message.answer("""📆 Введите дату продажи в формате ДД.ММ.ГГГГ:""")
        await state.set_state(DirectorStates.waiting_for_date)
    else:
        await message.answer("⛔ Неверный пароль! Повторно выберите роль при помощи /start")
        await state.clear()


# Ввод даты
@router.message(DirectorStates.waiting_for_date)
async def process_date(message: Message, state: FSMContext):
    date_text = message.text.strip()
    try:
        datetime.strptime(date_text, "%d.%m.%Y")
    except ValueError:
        await message.answer("⛔ Неверный формат даты! Используйте ДД.MM.ГГГГ.")
        return

    await state.update_data(date=date_text)
    await message.answer(
        "📈 Введите продажи через пробел в формате:\n"
        "груши, яблоки, апельсины, мандарины, ананасы\n\n"
        "📃 Например: 12 15 18 10 32"
    )
    await state.set_state(DirectorStates.waiting_for_sales)


# Ввод продаж
@router.message(DirectorStates.waiting_for_sales)
async def process_sales(message: Message, state: FSMContext):
    sales_text = message.text.strip()
    try:
        pears, apples, oranges, mandarins, pineapples = [
            int(x.strip()) for x in sales_text.split(" ")
        ]
    except ValueError:
        await message.answer("⛔ Ошибка! Нужно ввести 5 чисел через запятую.")
        return

    data = await state.get_data()
    store_id = data.get("store_id")
    date = data.get("date")

    if not store_id or not date:
        await message.answer("⛔ Вы не авторизованы или не ввели дату!")
        await state.clear()
        return

    try:
        print(f"[INFO] Вношу новые данные в таблицу Sales для магазина {store_id} за {date}...")
        await message.answer("⏳ Вношу изменения. Пожалуйста подождите...")
        await append_sales_row(
            date=date,
            store_id=store_id,
            pears=pears,
            apples=apples,
            oranges=oranges,
            mandarins=mandarins,
            pineapples=pineapples,
            user_id=message.from_user.id
        )
        print(f"[INFO] Данные успешно добавлены.")
        await message.answer("✅ Данные успешно добавлены!")
    except Exception as e:
        await message.answer(f"⛔ Ошибка при добавлении данных: {e}")
        return

    # После добавления продаж снова спрашиваем дату (зацикливаем ввод)
    await message.answer("Введите следующую дату продаж в формате ДД.MM.ГГГГ или /logout для выхода:")
    await state.set_state(DirectorStates.waiting_for_date)
