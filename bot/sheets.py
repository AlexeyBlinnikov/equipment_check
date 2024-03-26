from pprint import pprint
# import requests
# from binance import p2p, market
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'key_admin.json'
# ID Google Sheets документа (можно взять из его URL)
# spreadsheet_id = '1-mb5Eu72jKW8kWrwWnAr7BRrioE7OCVVEMUBI6SnPlg'
spreadsheet_id = "1it-gG3gWB1AjUhN4yTLVR-PaX7iHrmfqIZVtp7n9J3w"
spreadsheet_id_dekabristov = "1I_f2EeVp3HSxUibXblwvGb0WkZ8jMgnlkZX-ElgGkQg"

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


def append_values(range_name, fio, money, status="", eq="", start_date="", end_date=""):
    try:
        values = [
            [
                f"{fio}", f"{money}", f"{status}", f"{eq}", f"{start_date}", f"{end_date}"
            ],
        ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="USER_ENTERED", body=body).execute()
        # print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        print(f"Ошибка : {error}!!!!!!!!!!!!!!!")
        return error

def get_batch(range_name):
    try:
        # values = [
        #     [
        #         f"{x}"
        #     ],
        # ]
        body = {
            # 'values': values
        }
        result = service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id_dekabristov, ranges=range_name).execute()
        return result
    except HttpError as error:
        print(f"Ошибка : {error}!")
        return error

def update_value(range_name, x):
    try:
        values = [
            [
                f"{x}"
            ],
        ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id_dekabristov, range=range_name,
            valueInputOption="USER_ENTERED", body=body).execute()
        return result
    except HttpError as error:
        print(f"Ошибка : {error}!")
        return error

# def append_values(x):
#     try:
#         # values = [
#         #     [
#         #         f"{y}"
#         #     ],
#         # ]
#         #Найти ячейку 
#         result = service.spreadsheets().values('Значение') # я искал с датой

#         #Получение номера строки найденной ячейки
#         row_number = result.row

#         print("Номер строки: ", row_number) # мы великолепны
#         # rangex = x
#         # result = service.spreadsheets().values().batchGetByDataFilter(
#         #     spreadsheetId=spreadsheet_id, 
#         #         body = {

#         # "dataFilters": [
#         #     {
#         #         "developerMetadataLookup": {
#         #             "metadataValue": "01/01/2024",
#         #     },
#         #     #     "a1Range": "B1:E1"
#         #     }
#         # ],
#         # "majorDimension": "ROWS",
#         # "valueRenderOption": "FORMATTED_VALUE"
#         # }).execute()
#         # print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
#         return result

#     except HttpError as error:
#         print(f"Ошибка : {error}!!!!!!!!!!!!!!!")
#         return error


# # append_values("B4:D4", "1", 3, "5")




# # import google.auth
# # from googleapiclient.discovery import build
# # from googleapiclient.errors import HttpError


# def sheets_batch_update(spreadsheet_id, find, replacement):
#   """
#   Update the sheet details in batch, the user has access to.
#   Load pre-authorized user credentials from the environment.
#   TODO(developer) - See https://developers.google.com/identity
#   for guides on implementing OAuth2 for the application.
#   """

# #   creds, _ = google.auth.default()
#   # pylint: disable=maybe-no-member

#   try:
#     # service = build("sheets", "v4", credentials=creds)

#     requests = []
#     # Change the spreadsheet's title.
#     # requests.append(
#     #     {
#     #         "updateSpreadsheetProperties": {
#     #             # "properties": {"title": title},
#     #             "fields": "title",
#     #         }
#     #     }
#     # )
#     # Find and replace text
#     requests.append(
#         {
#             "findReplace": {
#                 "find": find,
#                 "replacement": replacement,
#                 "allSheets": True,
#             }
#         }
#     )
#     # Add additional requests (operations) ...

#     body = {"requests": requests}
#     response = (
#         service.spreadsheets()
#         .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
#         .execute()
#     )
#     find_replace_response = response.get("replies")[0].get("findReplace")
#     print(
#         f"{find_replace_response.get('occurrencesChanged')} replacements made."
#     )
#     return response

#   except HttpError as error:
#     print(f"An error occurred: {error}")
#     return error















# # # from aiogram.utils import executor
# # from aiogram import types
# # from create_bot import bot, dp
# # # from aiogram.types import ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton
# # import asyncio
# # import aioschedule
# # # from aiogram.dispatcher.filters import Text
# # from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
# #     get_user_locale
# # # from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback
# # from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
# # from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
# # from aiogram import types, F#, Router
# # from aiogram.types import Message
# # from aiogram.filters import Command
# # from aiogram.filters.callback_data import CallbackData
# # from datetime import datetime
# # from aiogram.fsm.context import FSMContext
# # from aiogram.fsm.state import State, StatesGroup






# # class FSMClient(StatesGroup):
# #     state_date = State()
# #     state_process = State()
# #     state_time = State()



# # async def set_masters(call: types.CallbackQuery):
# #     await call.message.delete_reply_markup()
# #     await call.message.delete()
# #     await call.message.answer(str.GET_MASTERS, reply_markup=keyboards_client.btn_add_masters)
# #     await FSMClient.state_date.set()

# # async def set_date(call: types.CallbackQuery):
# #     await call.message.delete_reply_markup()
# #     await call.message.delete()
# #     await call.message.answer(str.SET_DATE, reply_markup=await SimpleCalendar().start_calendar())
# #     await FSMClient.next()
    
# # async def process_dialog_calendar(call: types.CallbackQuery, callback_data: dict):
# #     selected, date = await SimpleCalendar().process_selection(call, callback_data)
# #     if selected:
# #         str.USER_DATE_SELECT = str.USER_DATE + f' {date.strftime("%d.%m.%Y")} \n'
# #         await call.message.answer(str.USER_DATE_SELECT)
# #     await FSMClient.next()

# # async def set_time(call: types.CallbackQuery):
# #     await call.message.delete()
# #     inline_timepicker.init(
# #         datetime.time(12),
# #         datetime.time(1),
# #         datetime.time(23),
# #     )

# #     await call.message.answer(text=str.YOUR_TIME,
# #                               reply_markup=inline_timepicker.get_keyboard())



# # def register_handlers_client(dp: Dispatcher):
# #     dp.register_callback_query_handler(set_date, state=FSMClient.state_date)
# #     dp.register_callback_query_handler(process_dialog_calendar, simple_cal_callback.filter(), state=FSMClient.state_process)
# #     dp.register_callback_query_handler(set_time, state=FSMClient.state_time)