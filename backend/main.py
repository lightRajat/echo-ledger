from app.routes import router
from app.silero import Silero
from app.whisper import Whisper
import asyncio # REMOVE LATER
from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect # REMOVE LATER
from utils import push_alternating_messages # REMOVE LATER
import uvicorn
import warnings
warnings.filterwarnings("ignore")

app = FastAPI()

silero = Silero()
app.state.silero = silero
whisper = Whisper(silero.audio_queue)

app.include_router(router)

# REMOVE LATER
print("Dashboard Websocket server listening")
@app.websocket("/dashboard")
async def dashboard(websocket: WebSocket):
    await websocket.accept()
    print("Connected to dashboard websocket")

    pusher_task = asyncio.create_task(push_alternating_messages(websocket))
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Client sent: {data}")
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pusher_task.cancel()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)