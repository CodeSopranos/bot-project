import os
import httpx
import uvicorn
import numpy as np
from fastapi import FastAPI, Request, File, UploadFile

from utils.predict import dummy_model, accent_model

app = FastAPI(title='The accent bot', description='English pronunciation scoring')

TOKEN = os.getenv("TG_TOKEN", None)  # Telegram Bot API Key
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID", '<some-chat-id>')  # Telegram Chat ID


@app.get("/ping/", tags=["Utils"])
async def ping(request: Request = None):
    return {"message": "PONG.", 'request': request.url.path}


@app.post("/set_webhook/", tags=["Utils"])
async def set_webhook(host: str):
    url = f"https://api.telegram.org/{TOKEN}/setWebhook?url={host}/api/"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url)
    return resp


@app.post("/api/send/", tags=["Utils"])
async def send(message: str = '*Hello*, _world_!', chat_id: str = OWNER_CHAT_ID):
    await tg_send_message(message, chat_id)
    return {'status': message}


@app.post("/api/predict/", tags=["Scoring"])
async def predict(audio: str = 'audio'):
    score = dummy_model.predict()
    most_relevant = ['en', 'ru', 'de']
    return {'score': score, 'most_relevant': most_relevant}


@app.post("/api/audio/denoise/", tags=["Audio"])
async def denoise_audio(audio: str = 'audio'):
    return {'status': "OK"}


@app.post("/api/audio/accent-recognition/", tags=["Audio"])
async def predict_accent(file: UploadFile = File(...)):
    try:
        result = accent_model.predict(file.file)
    except Exception as e:
        result = {'Error': str(e)}
    return result


@app.get("/api/get_sample/", tags=["Scoring"])
async def get_sample():
    sentence = accent_model.get_sample()
    return {'sample': sentence}


async def tg_send_message(message: str, chat_id: str):
    print(message)
    tg_msg = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=tg_msg)
    print(resp.json())
