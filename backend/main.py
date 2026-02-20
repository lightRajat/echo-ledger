import constants as c
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import queue
from silero_vad import load_silero_vad
from utils import Timer, stitch_audio_bytes
import torch
import uvicorn
import warnings
warnings.filterwarnings("ignore")

app = FastAPI()
vad_model = load_silero_vad()

audio_queue = queue.Queue()
audio_queue_buffer = []
audio_stitch_timer = Timer(c.SILENCE_THRESHOLD_MS / 1000, stitch_audio_bytes, audio_queue, audio_queue_buffer)

@app.websocket("/")
async def home(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            websocket_bytes = await websocket.receive_bytes()

            # silero vad
            torch_tensor = torch.frombuffer(websocket_bytes, dtype=torch.float32)
            speech_prob = vad_model(torch_tensor, c.SAMPLE_RATE).item()
            if speech_prob > 0.5:
                audio_queue_buffer.append(websocket_bytes)
                audio_stitch_timer.reset()

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)