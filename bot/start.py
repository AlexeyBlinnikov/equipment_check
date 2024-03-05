from operator import eq
from aiogram import types
import asyncio
import aioschedule
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
    get_user_locale
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from aiogram import types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import pandas
from datetime import date, timedelta
from sqlite_db import sql_start, sql_add_command, sql_read_date1_today, sql_read, get_all_categories, sql_read_rowid, del_sql, update_sql_extend, sql_read_date2, sql_read_date2_today
from create_bot import bot, dp
import sqlite3
import math

arr_equipment = []
arr_action = []
arr_extend = []
count_puzzi = 3
count_ps = 3


class Form(StatesGroup):
    start_date = State()
    last_date = State()
    name = State()
    price = State()

class Form1(StatesGroup):
    extend = State()

         #отмена ввода
@dp.message(Command("cancel"))
@dp.message(F.text.casefold() == "отмена")
async def cancel(message: types.Message, state: FSMContext):
    # if message.from_user.id == ID:
    current_state = await state.get_state()
    if current_state is None:
        return 
    await state.clear()
    await message.reply('Выход из машины состояний')

# @dp.message(Command("test"))
# async def send_test(message: types.Message):
#     await bot.send_message(message.from_user.id, text = f"Привет")


async def on_startup(_):
    print('Бот вышел в онлайн!')
    # asyncio.create_task(scheduler())
async def send_welcome(message: types.Message):
        await bot.send_message(message.from_user.id, "Выбери действие", reply_markup=start_kb.as_markup())
async def send_welcome_query(call: types.CallbackQuery):
        await bot.send_message(call.from_user.id, "Выбери действие", reply_markup=start_kb.as_markup())


# ___________Плавающие инлайн кнопки для Возврата и Продления___________
async def category_swipe_fp(remover, return_or_extend):
    get_categories = get_all_categories()
    keyboard = InlineKeyboardBuilder()
    if len(get_categories) == 0:
        keyboard.add(InlineKeyboardButton(text = "Нет оборудования в аренде."
                             ,callback_data="start_command"))
        return keyboard
    if remover >= len(get_categories): remover -= 10
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            # print(get_categories[a])
            keyboard.add(InlineKeyboardButton(text = f"{get_categories[a]['name']} : {get_categories[a]['equipment']} до {get_categories[a]['date2'][:-5]} 💵 {get_categories[a]['price']}"
                             ,callback_data=f"category_open_{get_categories[a]['rowid']}:{return_or_extend}:{get_categories[a]['name']}"))#:{get_categories[a]['date2']}"))
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            InlineKeyboardButton(text = f"💎 1/{math.ceil(len(get_categories) / 10)} 💎", callback_data="..."),
            InlineKeyboardButton(text = "Далее 👉", callback_data=f"category_swipe_{remover + 10}:{return_or_extend}"),#buy_category_swipe:{remover + 10}:{shop_id}"),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            InlineKeyboardButton(text = "👈 Назад", callback_data=f"category_swipe_{remover - 10}:{return_or_extend}"),
            InlineKeyboardButton(text = f"💎 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 💎", callback_data="..."),
        )
    else:
        keyboard.add(
            InlineKeyboardButton(text = "👈 Назад", callback_data=f"category_swipe_{remover - 10}:{return_or_extend}"),
            InlineKeyboardButton(text = f"💎 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 💎", callback_data="..."),
            InlineKeyboardButton(text = "Далее 👉", callback_data=f"category_swipe_{remover + 10}:{return_or_extend}"),
        )
    return keyboard

@dp.callback_query(F.data.startswith('category_open_'))
async def user_purchase_category_next_page(call: types.CallbackQuery, state: FSMContext) -> None:
    x = call.data.replace("category_open_", "")
    row_id = x.split(":")[0]
    value2 = x.split(":")[1]
    name = x.split(":")[2]
    if value2 == "return":
        await del_sql(row_id)
        await bot.send_message(call.from_user.id, f"*{name}* осуществил полный *возврат.*", reply_markup=start_kb.as_markup(), parse_mode= "Markdown")
    elif value2 == "extend":
        arr_extend.append(row_id)
        await state.set_state(Form1.extend)
        await bot.send_message(call.from_user.id, f"Срок продления для клиента *{name}*:", parse_mode= "Markdown")
    else:
        await bot.send_message(call.from_user.id, "Ошибка")
    await call.answer()


@dp.message(Form1.extend)
async def extend (message:types.Message, state: FSMContext):
    await state.update_data(extend=message.text)
    data = await state.get_data()
    # вытащить дату2 из sql и прибавить к этой дате параметр data
    start_date = datetime.strptime(sql_read_date2(arr_extend[-1])[0], '%d.%m.%Y')
    end_date = datetime.strftime(start_date + timedelta(days=int(data["extend"])), '%d.%m.%Y')

    await update_sql_extend(end_date, arr_extend[-1])
    await bot.send_message(message.from_user.id, text = f"Успешно продлили срок аренды на *{data['extend']}* суток", reply_markup=start_kb.as_markup(), parse_mode= "Markdown")
    await state.clear()

@dp.callback_query(F.data.startswith('category_swipe_'))
async def user_purchase_category_next_page(call: types.CallbackQuery):
    x = call.data.replace("category_swipe_", "")
    remover = x.split(":")[0]
    value2 = x.split(":")[1]
    y = await category_swipe_fp(int(remover), f'{value2}')
    y.adjust(1, 1)
    await call.message.edit_text("Категории",
                                 reply_markup= y.as_markup())




# _______________________________Открывваем__КАЛЕНДАРЬ______________________________________

# _____Открываем календарь для кнопки ВЗЯЛИ______
# Другое
async def start_kalendar(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    eq = callback_query.data.replace('button_take_', '')
    arr_equipment.append(f"{eq}")
    await state.set_state(Form.start_date)
    await bot.send_message(callback_query.from_user.id,
        "Дата брони: ",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(callback_query.from_user)).start_calendar())
    await callback_query.answer()




# # _______________________________САМ_КАЛЕНДАРЬ______________________________________
@dp.callback_query(SimpleCalendarCallback.filter(), Form.start_date)
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date1=f'{date.strftime("%d.%m.%Y")}') # Запись даты в "state".
        # await state.set_state(Form.last_date)
        await callback_query.message.answer(
        "Дата возврата: ",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(callback_query.from_user)).start_calendar()
    )
        await state.set_state(Form.last_date)
    await callback_query.answer()

@dp.callback_query(SimpleCalendarCallback.filter(), Form.last_date)
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date2=f'{date.strftime("%d.%m.%Y")}') # Запись даты в "state".

        await bot.send_message(callback_query.from_user.id, "ФИО Арендатора: ")
        await state.set_state(Form.name)
    await callback_query.answer()
# ________________________________________________________________

@dp.message(Form.name)
async def name_person (message:types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.price)
    await message.answer("Оплатили: ")


@dp.message(Form.price)
async def price (message:types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await sql_add_command([arr_equipment[-1], data['name'], data['date1'], data['date2'], data['price']])
    await state.clear()
    # date_time_obj1 = datetime.strptime(data['date1'], '%d.%m.%Y')
    # date_time_obj2 = datetime.strptime(data['date2'], '%d.%m.%Y')
    # x = pandas.date_range(date_time_obj1,date_time_obj2-timedelta(days=1),freq='d')
    await bot.send_message(message.from_user.id, f"Добавили: *{arr_equipment[-1]}*\n\nНа имя: *{data['name']}*\n\nДо: *{data['date2']}*", reply_markup=start_kb.as_markup(), parse_mode= "Markdown")




# _______________________________Клавиатура______________________________________
# Кнопки старта
start_kb = ReplyKeyboardBuilder().row(KeyboardButton(text = "Взяли"), KeyboardButton(text = "Вернули")).row(KeyboardButton(text = "Бронь"), KeyboardButton(text = "Продлили"))
# Инлайн кнопки
take_reserv_kb_button = InlineKeyboardBuilder().add(InlineKeyboardButton(text = "Другое", callback_data='button_take_other')).add(InlineKeyboardButton(text = 'PS 5', callback_data='button_take_ps5')).add(InlineKeyboardButton(text ='Клининг', callback_data='select_cleaning')).add(InlineKeyboardButton(text = 'Go Pro', callback_data='button_take_gopro')).add(InlineKeyboardButton(text = 'Тепловизор', callback_data='button_take_teplovisor'))
take_reserv_kb_button.adjust(1, 2)


# _______Синхронный код_______
# Вывод категорий
async def take_kb(message: types.Message):
    arr_action.append("Взяли")
    await bot.send_message(message.from_user.id, "Выбери категорию", reply_markup=take_reserv_kb_button.as_markup())
async def return_kb(message: types.Message):
    x = await category_swipe_fp(0, "return")
    x.adjust(1, 1)
    await bot.send_message(message.from_user.id, "Выбери категорию", reply_markup=x.as_markup())
async def reserv_kb(message: types.Message):
    arr_action.append("Бронь")
    await bot.send_message(message.from_user.id, "Выбери категорию", reply_markup=take_reserv_kb_button.as_markup())
async def extend_kb(message: types.Message):
    x = await category_swipe_fp(0, "extend")
    x.adjust(1, 1)
    await bot.send_message(message.from_user.id, "Выбери категорию", reply_markup=x.as_markup())



# _____________Кнопка ВЗЯЛИ ПРИ НАЛИЧИИ РАЗДЕЛЕНИЙ_____________
async def take_klining(callback_query: types.CallbackQuery):
        await bot.send_message(callback_query.from_user.id, "Выбери оборудование", reply_markup = InlineKeyboardBuilder().add(InlineKeyboardButton(text = 'Puzzi', callback_data = 'button_take_puzzi')).as_markup())
        await callback_query.answer()

# _____________Кнопка БРОНЬ ПРИ НАЛИЧИИ РАЗДЕЛЕНИЙ_____________
async def reserv_klining(callback_query: types.CallbackQuery):
        await bot.send_message(callback_query.from_user.id, "Выбери оборудование", reply_markup = InlineKeyboardBuilder().add(InlineKeyboardButton(text = 'Puzzi', callback_data = 'button_reserv_puzzi')).as_markup())
        await callback_query.answer()





# # ________Асинхронный код_________
async def send_reminder():
    # Получить список дат из mysql
    date_today = datetime.now().date()
    all_eq = sql_read()
    take_today = sql_read_date1_today(date_today.strftime("%d.%m.%Y"))
    return_today = sql_read_date2_today(date_today.strftime("%d.%m.%Y"))
    count, count1, count2 = 1, 1, 1
    all, t, r = "", "", ""
    for i in all_eq:
        all+=f"{count}: 🙎‍♂️: {i[1]} 🛠: {i[0]} 💵: {i[4]}\n"
        count+=1
    for i in take_today:
        t+=f"{count1}: 🙎‍♂️: {i[1]} 🛠: {i[0]} 💵: {i[4]}\n"
        count1+=1
    for i in return_today:
        r+=f"{count2}: 🙎‍♂️: {i[1]} 🛠: {i[0]} 💵: {i[4]}\n"
        count2+=1
    await bot.send_message(377590850, text = f"*Сегодня в аренде*\n {all}\n\n*Должны вернуть*\n{r}\n*Должны взять*\n{t}", parse_mode= "Markdown")

try:
    async def scheduler():
            # aioschedule.every().day.at("07:00").do(send_reminder)
            aioschedule.every(60).seconds.do(send_reminder)
            # aioschedule.every(6).hours.do(send_admin_message_delqr)
            while True:
                await aioschedule.run_pending()
                await asyncio.sleep(1)
except:
    print("Ошибка асинхронной функции")


def register_handlers_client(dp):
    # dp.message.register(help, Command("help"))
    dp.message.register(send_welcome, Command("start"))
    dp.message.register(take_kb, F.text == 'Взяли')
    dp.message.register(return_kb, F.text == 'Вернули')
    dp.message.register(reserv_kb, F.text == 'Бронь')
    dp.message.register(extend_kb, F.text == 'Продлили')

    dp.callback_query.register(send_welcome_query, F.data =='start_command')
    # разделение кнопок от КЛИНИНГА
    dp.callback_query.register(reserv_klining, F.data == "button_reserv_3")
    dp.callback_query.register(take_klining, F.data == "select_cleaning")

    # прямой выход к календарю
    dp.callback_query.register(start_kalendar, F.data.startswith('button_take_'))





async def main():
    register_handlers_client(dp)
    sql_start()
    asyncio.create_task(scheduler())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())