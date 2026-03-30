import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

# ---------------- CONFIG ----------------
TOKEN = "8679125605:AAGWbHnO8TU6_Qjj-mVhtAhgkOF8_ftZgXY"
ADMIN_IDS = [5916597178]  # kerakli adminlar listi

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ---------------- MAIN MENU ----------------
menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Mol go'shtli somsa 13.000uzs", callback_data="mol_somsa")],
    [InlineKeyboardButton(text="Tovuq go'shtli somsa 8.000uzs", callback_data="qoy_somsa")],
    [InlineKeyboardButton(text="Oshqovoqli somsa 6.000uzs", callback_data="oshqovoq_somsa")],
    [InlineKeyboardButton(text="Kartoshkali somsa 6.000uzs", callback_data="kartoshka_somsa")],
])

# ---------------- PHONE ----------------
phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Telefon raqam yuborish", request_contact=True)]],
    resize_keyboard=True
)

user_orders = {}

# ---------------- START ----------------
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum!\n\n🥟 Toshkent Tomchi Somsa botiga xush kelibsiz\n\nBuyurtma qilmoqchi bo'lgan taomni tanlang:",
        reply_markup=menu_keyboard
    )

# ---------------- SOMSA TYPES ----------------
@dp.callback_query(F.data == "mol_somsa")
async def mol(callback: types.CallbackQuery):
    user_orders[callback.from_user.id] = "Mol go'shtli somsa"
    await callback.message.answer("Mol go'shtli somsa tanlandi 🥟\n\nTelefon raqamingizni yuboring", reply_markup=phone_keyboard)

@dp.callback_query(F.data == "qoy_somsa")
async def qoy(callback: types.CallbackQuery):
    user_orders[callback.from_user.id] = "Qo'y go'shtli somsa"
    await callback.message.answer("Qo'y go'shtli somsa tanlandi 🐑\n\nTelefon raqamingizni yuboring", reply_markup=phone_keyboard)

@dp.callback_query(F.data == "oshqovoq_somsa")
async def oshqovoq(callback: types.CallbackQuery):
    user_orders[callback.from_user.id] = "Oshqovoqli somsa"
    await callback.message.answer("Oshqovoqli somsa tanlandi 🎃\n\nTelefon raqamingizni yuboring", reply_markup=phone_keyboard)

@dp.callback_query(F.data == "kartoshka_somsa")
async def kartoshka(callback: types.CallbackQuery):
    user_orders[callback.from_user.id] = "Kartoshkali somsa"
    await callback.message.answer("Kartoshkali somsa tanlandi 🥔\n\nTelefon raqamingizni yuboring", reply_markup=phone_keyboard)

# ---------------- CONTACT ----------------
@dp.message(F.contact)
async def contact(message: types.Message):
    user_id = message.from_user.id
    phone = message.contact.phone_number
    food = user_orders.get(user_id, "Noma'lum")
    text = f"""
🛒 Yangi buyurtma

👤 Ism: {message.from_user.full_name}
📱 Telefon: {phone}
🍽 Taom: {food}
🆔 User ID: {user_id}
"""
    for admin in ADMIN_IDS:
        await bot.send_message(admin, text)

    await message.answer("✅ Buyurtma qabul qilindi!\nTez orada siz bilan bog'lanamiz.", reply_markup=types.ReplyKeyboardRemove())

# ---------------- HTTP SERVER (Render port uchun) ----------------
PORT = int(os.getenv("PORT", 8000))

async def handle(request):
    return web.Response(text="Bot running!")

app = web.Application()
app.add_routes([web.get("/", handle)])

# ---------------- RUN ----------------
async def main():
    print("Bot ishga tushdi...")
    loop = asyncio.get_event_loop()
    loop.create_task(web._run_app(app, port=PORT))  # fon server
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
