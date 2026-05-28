import asyncio

# Fix for Python 3.14 asyncio compatibility
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import os
from dotenv import load_dotenv
from pyrogram import Client, filters

# Load environment variables
load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

app1 = Client(
    "my_account",
    api_id=api_id,
    api_hash=api_hash
)

app2 = Client(
    "my_second_account",
    api_id=api_id,
    api_hash=api_hash
)


# ============ APP1 HANDLERS ============
@app1.on_message(filters.command("hello") & filters.private)
async def hello(client, message):
    await message.reply("Hello from Pyrogram!")


@app1.on_message(filters.command("info") & filters.private)
async def info(client, message):
    async for msg in client.get_chat_history(message.chat.id, limit=5):
        print(f"\n{'=' * 50}")
        print(f"Message ID: {msg.id}")
        print(f"From User ID: {msg.from_user.id if msg.from_user else 'N/A'}")
        print(f"From Username: @{msg.from_user.username if msg.from_user and msg.from_user.username else 'N/A'}")
        print(f"Date: {msg.date}")
        print(f"Text: {msg.text if msg.text else 'No text'}")
        print(f"Caption: {msg.caption if msg.caption else 'No caption'}")

        # Inline кнопки
        if msg.reply_markup:
            print(f"Reply Markup: {msg.reply_markup}")
            if hasattr(msg.reply_markup, 'inline_keyboard'):
                print("Inline Keyboard:")
                for row in msg.reply_markup.inline_keyboard:
                    for button in row:
                        print(f"  Button Text: {button.text}")
                        print(f"  Button URL: {button.url if button.url else 'None'}")
                        print(f"  Button Callback Data: {button.callback_data if button.callback_data else 'None'}")
                        print(f"  Button Type: {type(button).__name__}")

        # Медиа
        if msg.photo:
            print(f"Photo: {msg.photo.file_id}")
        if msg.video:
            print(f"Video: {msg.video.file_id}")
        if msg.document:
            print(f"Document: {msg.document.file_id}")
        if msg.audio:
            print(f"Audio: {msg.audio.file_id}")
        if msg.voice:
            print(f"Voice: {msg.voice.file_id}")
        if msg.sticker:
            print(f"Sticker: {msg.sticker.file_id}")
        if msg.animation:
            print(f"Animation: {msg.animation.file_id}")

        print(f"Entities: {msg.entities if msg.entities else 'None'}")
        print(f"Forward From: {msg.forward_from.id if msg.forward_from else 'None'}")
        print(f"Reply to Message ID: {msg.reply_to_message_id if msg.reply_to_message_id else 'None'}")

    await message.reply("Информация о последних 3 сообщениях выведена в консоль")


@app1.on_message(filters.command("click") & filters.private)
async def click_infinite(client, message):
    chat_id = message.chat.id
    button_names = [
        "Алтарь",
        "Мои питомцы",
        "Алтарь",
        "Призыв"
    ]

    await message.reply("Начинаю бесконечно прожимать 3 кнопки с интервалом 10 секунд...")

    while True:
        for button_name in button_names:
            target_button = None
            target_msg = None

            async for msg in client.get_chat_history(chat_id, limit=100):
                if msg.reply_markup and msg.reply_markup.inline_keyboard:
                    for row in msg.reply_markup.inline_keyboard:
                        for button in row:
                            if button_name.lower() in button.text.lower():
                                target_button = button
                                target_msg = msg
                                break
                        if target_button:
                            break
                if target_button:
                    break

            if target_button and target_msg:
                try:
                    await client.request_callback_answer(
                        chat_id=chat_id,
                        message_id=target_msg.id,
                        callback_data=target_button.callback_data
                    )
                    print(f"Кнопка '{button_name}' нажата")
                except Exception as e:
                    print(f"Ошибка для кнопки '{button_name}': {e}")
            else:
                print(f"Кнопка '{button_name}' не найдена")

            await asyncio.sleep(60)


# ============ APP2 HANDLERS ============
@app2.on_message(filters.command("hello") & filters.private)
async def hello2(client, message):
    await message.reply("Hello from Second Account!")


@app2.on_message(filters.command("info") & filters.private)
async def info2(client, message):
    async for msg in client.get_chat_history(message.chat.id, limit=5):
        print(f"\n[APP2] {'=' * 50}")
        print(f"Message ID: {msg.id}")
        print(f"From User ID: {msg.from_user.id if msg.from_user else 'N/A'}")
        print(f"From Username: @{msg.from_user.username if msg.from_user and msg.from_user.username else 'N/A'}")
        print(f"Date: {msg.date}")
        print(f"Text: {msg.text if msg.text else 'No text'}")

        if msg.reply_markup and hasattr(msg.reply_markup, 'inline_keyboard'):
            print("Inline Keyboard:")
            for row in msg.reply_markup.inline_keyboard:
                for button in row:
                    print(f"  Button Text: {button.text}")
                    print(f"  Button Callback Data: {button.callback_data if button.callback_data else 'None'}")

    await message.reply("Информация выведена в консоль [APP2]")


@app2.on_message(filters.command("click") & filters.private)
async def click_infinite2(client, message):
    chat_id = message.chat.id
    button_names = [
        "Кнопка 1",
        "Кнопка 2",
        "Кнопка 3"
    ]

    await message.reply("APP2: Начинаю прожимать кнопки с интервалом 60 секунд...")

    while True:
        for button_name in button_names:
            target_button = None
            target_msg = None

            async for msg in client.get_chat_history(chat_id, limit=100):
                if msg.reply_markup and msg.reply_markup.inline_keyboard:
                    for row in msg.reply_markup.inline_keyboard:
                        for button in row:
                            if button_name.lower() in button.text.lower():
                                target_button = button
                                target_msg = msg
                                break
                        if target_button:
                            break
                if target_button:
                    break

            if target_button and target_msg:
                try:
                    await client.request_callback_answer(
                        chat_id=chat_id,
                        message_id=target_msg.id,
                        callback_data=target_button.callback_data
                    )
                    print(f"[APP2] Кнопка '{button_name}' нажата")
                except Exception as e:
                    print(f"[APP2] Ошибка для кнопки '{button_name}': {e}")
            else:
                print(f"[APP2] Кнопка '{button_name}' не найдена")

            await asyncio.sleep(60)


async def main():
    await app1.start()
    await app2.start()

    me1 = await app1.get_me()
    me2 = await app2.get_me()
    print(f"APP1: @{me1.username} | APP2: @{me2.username}")
    print("Both accounts running...")

    await asyncio.gather(
        app1.idle(),
        app2.idle()
    )


if __name__ == "__main__":
    asyncio.run(main())