# # from aiogram.utils import executor
# from aiogram import types
# from create_bot import bot, dp
# # from aiogram.types import ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton
# import asyncio
# import aioschedule
# # from aiogram.dispatcher.filters import Text
# from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
#     get_user_locale
# # from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback
# from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
# from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
# from aiogram import types, F#, Router
# from aiogram.types import Message
# from aiogram.filters import Command
# from aiogram.filters.callback_data import CallbackData
# from datetime import datetime
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup






# class FSMClient(StatesGroup):
#     state_date = State()
#     state_process = State()
#     state_time = State()



# async def set_masters(call: types.CallbackQuery):
#     await call.message.delete_reply_markup()
#     await call.message.delete()
#     await call.message.answer(str.GET_MASTERS, reply_markup=keyboards_client.btn_add_masters)
#     await FSMClient.state_date.set()

# async def set_date(call: types.CallbackQuery):
#     await call.message.delete_reply_markup()
#     await call.message.delete()
#     await call.message.answer(str.SET_DATE, reply_markup=await SimpleCalendar().start_calendar())
#     await FSMClient.next()
    
# async def process_dialog_calendar(call: types.CallbackQuery, callback_data: dict):
#     selected, date = await SimpleCalendar().process_selection(call, callback_data)
#     if selected:
#         str.USER_DATE_SELECT = str.USER_DATE + f' {date.strftime("%d.%m.%Y")} \n'
#         await call.message.answer(str.USER_DATE_SELECT)
#     await FSMClient.next()

# async def set_time(call: types.CallbackQuery):
#     await call.message.delete()
#     inline_timepicker.init(
#         datetime.time(12),
#         datetime.time(1),
#         datetime.time(23),
#     )

#     await call.message.answer(text=str.YOUR_TIME,
#                               reply_markup=inline_timepicker.get_keyboard())



# def register_handlers_client(dp: Dispatcher):
#     dp.register_callback_query_handler(set_date, state=FSMClient.state_date)
#     dp.register_callback_query_handler(process_dialog_calendar, simple_cal_callback.filter(), state=FSMClient.state_process)
#     dp.register_callback_query_handler(set_time, state=FSMClient.state_time)