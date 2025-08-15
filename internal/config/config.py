import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GSHEET_ID = os.getenv("GSHEET_ID")


def get_sheet(sheet_name: str):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_path = Path(__file__).parent.parent.parent / "credentials.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(str(creds_path), scope)
    client = gspread.authorize(creds)
    return client.open_by_key(GSHEET_ID).worksheet(sheet_name)


def load_stores_data():
    """
    Читает лист Stores и возвращает два словаря:
    1) STORE_PASSWORDS: password -> store_id
    2) STORE_INFO: store_id -> {остальная информация}
    """
    sheet = get_sheet("Stores")
    rows = sheet.get_all_records()

    required_cols = {"store_id", "name", "pears_plan", "apples_plan",
                     "oranges_plan", "mandarins_plan", "pineapples_plan", "password"}
    if not required_cols.issubset(rows[0].keys()):
        raise ValueError(f"В листе Stores нет колонок: {required_cols}")

    store_passwords = {}
    store_info = {}

    for row in rows:
        store_id = row["store_id"]
        password = row["password"]

        # 1. словарь паролей
        if password:
            store_passwords[password] = store_id

        # 2. словарь с полной информацией
        store_info[store_id] = {
            "name":             row["name"],
            "pears_plan":       row["pears_plan"],
            "apples_plan":      row["apples_plan"],
            "oranges_plan":     row["oranges_plan"],
            "mandarins_plan":   row["mandarins_plan"],
            "pineapples_plan":  row["pineapples_plan"],
        }

    return store_passwords, store_info


# Генерируем словари при старте
STORE_PASSWORDS, STORE_INFO = load_stores_data()