import os
import httpx
import uvicorn
from fastapi import FastAPI, Request


app = FastAPI(title='The accent bot', description='English pronunciation scoring via chat-bot')

TOKEN = os.getenv("TG_TOKEN", None)  # Telegram Bot API Key
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID", '<some-chat-id>')  # Telegram Chat ID


@app.post("/set_webhook/")
async def set_webhook(host: str):
    url = f"https://api.telegram.org/{TOKEN}/setWebhook?url={host}/api/"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url)
    return resp


@app.post("/api/send/")
async def send(message: str = '*Hello*, _world_!', chat_id: str = OWNER_CHAT_ID):
    await tg_send_message(message, chat_id)
    return {'status': message}


async def tg_send_message(message: str, chat_id: str):
    print(message)
    tg_msg = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=tg_msg)
    print(resp.json())
