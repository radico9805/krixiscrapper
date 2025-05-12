import os
import pytesseract
import unicodedata
from telethon import TelegramClient, events
from PIL import Image
from io import BytesIO

# API credentials from https://my.telegram.org
api_id = 27164292
api_hash = '857d037ef546396f038980eeef6169a0'
session_name = 'krixi_session'

# Channels (as integers, NOT strings)
source_channel = -1002373156614
target_channel = -1002503432839

# Initialize client
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    text_content = ""
    
    if event.photo:
        buffer = BytesIO()
        await event.download_media(file=buffer)
        buffer.seek(0)
        img = Image.open(buffer)
        ocr_text = pytesseract.image_to_string(img)
        text_content += ocr_text.strip() + "\n\n"

    if event.raw_text:
        text_content += event.raw_text

    # Normalize text to plain characters
    def normalize_text(text):
        return ''.join(
            c for c in unicodedata.normalize('NFKD', text)
            if not unicodedata.combining(c)
        )

    normalized = normalize_text(text_content)

    # Remove unwanted lines like 'DEBIT 2)' and 'a8 »'
    lines = normalized.splitlines()
    cleaned_lines = [
        line for line in lines
        if not line.strip().lower().startswith("debit") and not line.strip().endswith("»")
    ]
    cleaned_text = "\n".join(cleaned_lines)

    # Replace phrases
    cleaned_text = (
        cleaned_text
        .replace("Scrapper Free Cxrti", "krixi scrapper")
        .replace("Scrapper by", "Scrapper by Lucius♥️")
        .replace("LxCxrti", "Lucius♥️")
    )

    if cleaned_text.strip():
        await client.send_message(target_channel, cleaned_text.strip())

print("✅ Krixi Scraper running... Ctrl+C to stop.")
client.start()
client.run_until_disconnected()
