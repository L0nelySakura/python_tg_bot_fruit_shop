import pandas as pd
from internal.config.config import STORE_INFO
from internal.services.gsheet import get_sales_data


async def generate_sales_report_excel(month: int, year: int) -> str:
    print(f"[INFO] Генерирую план продаж за {month:02}.{year}...")
    # Получаем все продажи
    sales_data = get_sales_data()  # все данные из Sales

    # Превращаем в DataFrame
    df = pd.DataFrame(sales_data)

    # Оставляем только данные за нужный месяц и год
    df['date'] = pd.to_datetime(df['date'], format="%d.%m.%Y")
    df = df[(df['date'].dt.month == month) & (df['date'].dt.year == year)]

    # Группируем по магазину
    report = []
    for store_id, group in df.groupby('store_id'):
        store = STORE_INFO.get(store_id, {})
        row = {'store_id': store_id, 'store_name': store.get('name', '')}
        total_plan = 0
        total_sales = 0
        for fruit in ['pears', 'apples', 'oranges', 'mandarins', 'pineapples']:
            fruit_sales = group[fruit].sum()
            fruit_plan = store.get(f'{fruit}_plan', 0)
            pct = round(fruit_sales / fruit_plan * 100, 2) if fruit_plan else 0
            row[f'{fruit}_percentage'] = f"{pct}%"
            total_sales += fruit_sales
            total_plan += fruit_plan
        row['total_percentage'] = f"{round(total_sales/total_plan * 100, 2) if total_plan else 0}%"
        report.append(row)

    report_df = pd.DataFrame(report)

    # Сохраняем в Excel
    file_path = f"output/sales_report_{month:02}_{year}.xlsx"
    print(f"[INFO] Сохраняю план продаж в {file_path}...")
    report_df.to_excel(file_path, index=False)
    print(f"[INFO] Успешно сохранено.")
    return file_path
