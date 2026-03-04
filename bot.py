import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

TOKEN = "8581609119:AAFxqO3I3mh1xPnkNr-HLS5vOk4N0UogF8I"
ADMIN_ID = 184521892  # O'Z TELEGRAM IDINGIZ

bot = Bot(token=TOKEN)
dp = Dispatcher()

reply_state = {}


# ===== START =====
@dp.message(Command("start"))
async def start_handler(message: Message):
    # Agar admin bo‘lsa — hech narsa chiqmaydi
    if message.from_user.id == ADMIN_ID:
        return

    await message.answer("Xabaringizni yozing")


# ===== USER XABAR YUBORADI =====
@dp.message(F.from_user.id != ADMIN_ID)
async def forward_to_admin(message: Message):
    # Faqat text xabarlarni qabul qiladi
    if not message.text:
        return

    user = message.from_user

    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name if user.last_name else ""
    username = f"@{user.username}" if user.username else "Yo‘q"
    profile_link = f"https://t.me/{user.username}" if user.username else "Username yo‘q"

    text = (
        f"📩 YANGI XABAR\n\n"
        f"👤 Ismi: {first_name} {last_name}\n"
        f"🆔 ID: {user_id}\n"
        f"🔗 Username: {username}\n"
        f"🌐 Profil link: {profile_link}\n\n"
        f"📝 Xabar:\n{message.text}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✉️ Javob berish",
                    callback_data=f"reply_{user_id}"
                )
            ]
        ]
    )

    await bot.send_message(ADMIN_ID, text, reply_markup=keyboard)
    await message.answer("✅ Xabaringiz yuborildi.")


# ===== ADMIN TUGMANI BOSADI =====
@dp.callback_query(F.data.startswith("reply_"))
async def start_reply(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    user_id = int(callback.data.split("_")[1])
    reply_state[ADMIN_ID] = user_id

    await callback.message.answer("✏️ Javob yozing:")
    await callback.answer()


# ===== ADMIN JAVOB YOZADI =====
@dp.message(F.from_user.id == ADMIN_ID)
async def send_reply(message: Message):
    # Agar reply rejimda bo‘lmasa — hech narsa qilmaydi
    if ADMIN_ID not in reply_state:
        return

    user_id = reply_state[ADMIN_ID]

    await bot.send_message(
        user_id,
        f"📩 Admin javobi:\n\n{message.text}"
    )

    await message.answer("✅ Javob yuborildi.")
    del reply_state[ADMIN_ID]


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())