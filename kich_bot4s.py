import asyncio
import json
import logging
import os
import sys
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from datetime import datetime
from aiogram.types import Chat, User, ChatMemberMember
from aiogram.filters import Command
from config_bot import * 

# /test_chat_member - команда імітування підписки

LEAD_MAGNET_FILE = "lead_magnet.json"
TEST_PERIOD_FILE = "test_period.json"


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
# Реєструємо бота в диспетчері (необхідно для aiogram 3.x)
dp.bot = bot

@dp.message(Command("test"))
async def test_command(message: types.Message): # перевірка чи працюють команди взагалі
    logging.info("--- test command triggered ---")
    await message.reply("Команды:\n/test_chat_member - команда имитации подписки\n/debug - сброс таймеров")

def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

def remove_user_from_file(file_name, user_id):
    """Видаляє користувача з JSON-файлу"""
    data = load_data(file_name)
    if str(user_id) in data:
        del data[str(user_id)]
        save_data(file_name, data)
        logging.info(f"Користувач {user_id} видалений з {file_name}")
    else:
        logging.info(f"Користувача {user_id} немає в {file_name}")

def remove_user_from_lead_magnet(user_id):
    remove_user_from_file(LEAD_MAGNET_FILE, user_id)

def remove_user_from_test_period(user_id):
    remove_user_from_file(TEST_PERIOD_FILE, user_id)

async def send_message_to_channel(bot, channel_id, text):
    await bot.send_message(chat_id=channel_id, text=text)

@dp.message(Command("debug"))
async def debug_command(message: types.Message):
    for file in [LEAD_MAGNET_FILE, TEST_PERIOD_FILE]:
        if os.path.exists(file):
            os.remove(file)
    await message.reply("Debug: JSON файлы таймеров удалены.")

async def shutdown_bot():
    print("Бот вимикається...")
    sys.exit()    

@dp.chat_member()
async def on_chat_member_update(update: ChatMemberUpdated):
    chat_cnl = await bot.get_chat(CHANNEL_USERNAME)
    chat_id = update.chat.id  # ID каналу
    new_member = update.new_chat_member
    user_id = new_member.user.id
    status = new_member.status  # Новий статус користувача

    if chat_id != chat_cnl.id:
        return
    logging.info(f"Користувач {user_id} змінив статус у каналі {chat_id}: {status}")

    if status in ["member", "administrator"]: #!!!!!! no , "creator" !!!
        # У aiogram 3.x клавіатури створюються інакше
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=LID_BTN, callback_data=f"lead_{user_id}")]
        ])
        await bot.send_message(user_id, BGN_TXT, reply_markup=keyboard)

# ця команда імітує приписку нового користувача, 
# щоб не відписуватись, а потім приписуватись під час відлагоджування і тестування бота
@dp.message(Command("test_chat_member"))
async def test_chat_member_update(message: types.Message):
    chat_cnl = await bot.get_chat(CHANNEL_USERNAME)  # Отримуємо інформацію про канал

    # У новій версії aiogram необхідно створити об'єкт ChatMemberUpdated по-іншому
    fake_update = ChatMemberUpdated(
        chat=Chat(id=chat_cnl.id, type="supergroup", title=chat_cnl.title),
        from_user=User(id=message.from_user.id, is_bot=False, first_name="TestUser"),
        date=datetime.now(),
        old_chat_member=ChatMemberMember(
            user=User(id=message.from_user.id, is_bot=False, first_name="TestUser"),
            status="member"
        ),
        new_chat_member=ChatMemberMember(
            user=User(id=message.from_user.id, is_bot=False, first_name="TestUser"),
            status="member"
        )
    )

    await on_chat_member_update(fake_update)

@dp.callback_query(F.data.startswith("lead_"))
async def send_lead_magnet(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = load_data(LEAD_MAGNET_FILE)
    now = datetime.now().timestamp()
    
    if str(user_id) not in data:
        data[str(user_id)] = {"time": now, "step": 1}
        save_data(LEAD_MAGNET_FILE, data)
    # Завжди створюємо кнопки, навіть якщо користувач уже є в базі
    if(TEST_BTN_ENABLE!=0):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=BAY_BTN, callback_data=f"buy_{user_id}")],
            [InlineKeyboardButton(text=RENT_BTN, callback_data=f"rent_{user_id}")],
            [InlineKeyboardButton(text=TEST_BTN, callback_data=f"test_{user_id}")]
        ])
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=BAY_BTN, callback_data=f"buy_{user_id}")],
            [InlineKeyboardButton(text=RENT_BTN, callback_data=f"rent_{user_id}")]
        ])

    await bot.send_message(user_id, LID_TXT, reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query(F.data.startswith("buy_"))
async def buy_now(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(user_id, BAY_TXT)
    await callback_query.answer()
    remove_user_from_lead_magnet(user_id)
    remove_user_from_test_period(user_id)

@dp.callback_query(F.data.startswith("rent_"))
async def rent_bot(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(user_id, "Вот ссылка на оплату ($15/мес).")
    await callback_query.answer()
    remove_user_from_lead_magnet(user_id)
    remove_user_from_test_period(user_id)

@dp.callback_query(F.data.startswith("test_"))
async def start_test_period(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = load_data(TEST_PERIOD_FILE)
    now = datetime.now().timestamp()
    remove_user_from_lead_magnet(user_id)
    
    if str(user_id) not in data:
        data[str(user_id)] = {"time": now, "step": 1}
        save_data(TEST_PERIOD_FILE, data)
        await bot.send_message(user_id, TEST1_TXT)
    await bot.send_message(user_id, TEST2_TXT)
    await callback_query.answer()

async def check_timers():
    while True:
        await asyncio.sleep(1)
        now = datetime.now().timestamp()
        
        lead_data = load_data(LEAD_MAGNET_FILE)
        for user_id, info in list(lead_data.items()):
            elapsed = now - info["time"]
            if info["step"] == 1 and elapsed >= LID_TIME1:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Бери бота за $100 - время денег", callback_data=f"buy_{user_id}")],
                    [InlineKeyboardButton(text="Аренда за $15/мес", callback_data=f"rent_{user_id}")]
                ])
                await bot.send_message(user_id, LID_TIME1_TXT, reply_markup=keyboard)
                # ще додаємо кнопку
                #lead_data[user_id]["time"] = now
                lead_data[user_id]["step"] = 2
            elif info["step"] == 2 and elapsed >= LID_TIME2:
                await bot.send_message(int(user_id), LID_TIME2_TXT)
                lead_data[user_id]["step"] = 0  # Отключаем таймер для этого пользователя
        save_data(LEAD_MAGNET_FILE, lead_data)
        
        test_data = load_data(TEST_PERIOD_FILE)
        for user_id, info in list(test_data.items()):
            elapsed = now - info["time"]
            if info["step"] == 1 and elapsed >= TEST_TIME1: # 10 днів
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Аренда за $15/мес", callback_data=f"rent_{user_id}")]
                ])                
                await bot.send_message(user_id, TEST_TIME1_TXT, reply_markup=keyboard)
                #test_data[user_id]["time"] = now  
                test_data[user_id]["step"] = 2
            elif info["step"] == 2 and elapsed >= TEST_TIME2: # 14 днів
                await bot.send_message(int(user_id), TEST_TIME2_TXT)
                test_data[user_id]["step"] = 0 # Отключаем таймеры для теста 
                await send_message_to_channel(bot, CHANNEL_ID_1, "Тестовый период завершился для "+CHANNEL_USERNAME)
                # --- це тільки для тих, хто продає боти ---
                #await shutdown_bot() # це тільки для тих, хто продає боти !

        save_data(TEST_PERIOD_FILE, test_data)

async def main():
    logging.info("V4 Бот запущено...")
    asyncio.create_task(check_timers())
    logging.info("Таймери перевірки запущені.")
    # Адаптація для aiogram 3.x - додаємо бота до диспетчера при старті
    await dp.start_polling(bot, allowed_updates=["message", "callback_query", "chat_member"])

if __name__ == "__main__":
    asyncio.run(main())