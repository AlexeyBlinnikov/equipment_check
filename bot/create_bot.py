from aiogram import Bot
from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.types import Message
from aiogram import types
import asyncio
from aiogram.filters import Command

router = Router()

TOKEN = "5524654123:AAHfHmtyG1-s1G0JtZFbQX7FInrgh9fo50g"


bot = Bot(token = TOKEN) 
dp = Dispatcher()

dp.include_router(router)




















# dp = Router(bot)

# @router.message(Command("start"))
# async def cmd_start(message: types.Message):
#     kb = [
#         [types.InlineKeyboardButton(text="С пюрешкоfwgfasgadsй")],
#         [types.InlineKeyboardButton(text="Без пюрешки")]
#     ]
#     keyboard = types.InlineKeyboardBuilder(keyboard=kb)
#     await message.answer("sgvjn", reply_markup=keyboard)



# ________________________________
# builder = InlineKeyboardBuilder().add(InlineKeyboardButton(text="Нажми меня",callback_data="random_value")).add(InlineKeyboardButton(text="Нажми меня",callback_data="random_value"))

# @dp.message(Command("random"))
# async def cmd_random(message: types.Message):
#     await message.answer(
#         "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
#         reply_markup=builder.as_markup()
#     )


# builder = ReplyKeyboardBuilder().add(KeyboardButton(text="Нажми меня"))#.add(InlineKeyboardButton(text="Нажми меня",callback_data="random_value"))

# @dp.message(Command("random"))
# async def cmd_random(message: types.Message):
#     await message.answer(
#         "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
#         reply_markup=builder.as_markup()
#     )
# _______________________




# async def main():
#     bot = Bot(token=TOKEN)
#     dp = Dispatcher()#storage=MemoryStorage())
#     dp.include_router(router)
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

# from aiogram import types, F, Router
# from aiogram.types import Message
# from aiogram.filters import Command


# @router.message(Command("start"))
# async def start_handler(msg: Message):
#     await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")


# @router.message()
# async def message_handler(msg: Message):
#     await msg.answer(f"Твой ID: {msg.from_user.id}", reply_markup=builder.as_markup())


# if __name__ == "__main__":
#     # logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())

# async def main():
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


# # register_handlers_client(dp)
# # dp.start_polling(bot, on_startup = on_startup)
# if __name__ == "__main__":
#     # logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())