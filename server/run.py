import os
import httpx
import uvicorn
from fastapi import FastAPI, Request


import uvicorn


app = FastAPI()

TOKEN = os.getenv("TG_TOKEN", None)  # Telegram Bot API Key
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID", '<some-chat-id>')  # Telegram Chat ID

async def sendTgMessage(message: str, chat_id: str):
    print(message)
    tg_msg = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        resp = await client.post(API_URL, json=tg_msg)
    print(resp.json())

@app.post("/send/")
async def send(message: str = '*Hello*, _world_!', chat_id: str = OWNER_CHAT_ID):
    await sendTgMessage(message, chat_id)
    return {'status': message}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)#, reload=True)