from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import requests, os, tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# التوكن والـ Chat ID هيتم قراءتهم من إعدادات Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.post("/upload")
async def upload(video: UploadFile = File(...)):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
    tmp.write(await video.read())
    tmp.close()

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(tmp.name, "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"video": f})

    os.remove(tmp.name)
    return {"status": "ok"}

@app.get("/")
def home():
    return {"status": "server running"}
