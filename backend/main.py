from const import SAMPLE_RATE
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from silero_vad import load_silero_vad
import torch
import uvicorn
import warnings
warnings.filterwarnings("ignore")

app = FastAPI()
vad_model = load_silero_vad()

@app.websocket("/")
async def home(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            websocket_bytes = await websocket.receive_bytes()
            torch_tensor = torch.frombuffer(websocket_bytes, dtype=torch.float32)
            speech_prob = vad_model(torch_tensor, SAMPLE_RATE).item()
            if speech_prob > 0.5:
                print("Speech detected")

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)