import os
import pytesseract
from telethon import TelegramClient, events
from PIL import Image
from io import BytesIO
import asyncio

# API credentials
api_id = 27164292
api_hash = '857d037ef546396f038980eeef6169a0'
session_name = 'krixi_session'

# Channels (as integers)
source_channel = -1002373156614
target_channel = -1002503432839

# Initialize client
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    text_content = ""
    
    if event.photo:
        file = await event.download_media(bytes)
        img = Image.open(BytesIO(file))
        ocr_text = pytesseract.image_to_string(img)
        text_content += ocr_text.strip() + "\n\n"

    if event.message.message:
        text_content += event.message.message

    text_content = text_content.replace("Scrapper Free Cxrti", "krixi scrapper")

    if text_content.strip():
        await client.send_message(target_channel, text_content.strip())

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ Session not authorized. Please create the session locally and upload it.")
        return

    print("✅ Krixi Scraper running... Ctrl+C to stop.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
