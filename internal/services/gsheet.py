import gspread
from oauth2client.service_account import ServiceAccountCredentials
from internal.config.config import GSHEET_ID
import datetime


def get_sheet(sheet_name: str):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_key(GSHEET_ID).worksheet(sheet_name)


async def append_sales_row(date, store_id, pears, apples, oranges, mandarins, pineapples, user_id):
    sheet = get_sheet("Sales")
    sheet.append_row([
        date,
        store_id,
        pears,
        apples,
        oranges,
        mandarins,
        pineapples,
        user_id
    ])


def get_sales_data():
    sheet = get_sheet("Sales")
    return sheet.get_all_records()
