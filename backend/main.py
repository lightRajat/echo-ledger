from app.silero import Silero
from app.llama import Llama
from app.routes import router
from app.utils import log
from app.whisper import Whisper
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
import os
import uvicorn
import warnings
warnings.filterwarnings("ignore")

app = FastAPI()

silero = Silero()
app.state.silero = silero
whisper = Whisper(silero.audio_queue, device='gpu')
llama = Llama(whisper.text_queue, os.getenv("LLAMA_REPO_ID"), os.getenv("LLAMA_FILE_NAME"))

app.include_router(router)
log("Websockets active")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)