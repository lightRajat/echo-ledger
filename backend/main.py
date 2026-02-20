import constants as c
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from faster_whisper import WhisperModel
import queue
from silero_vad import load_silero_vad
from utils import Timer, stitch_audio_bytes, transcribe_audio
import threading
import torch
import uvicorn
import warnings
warnings.filterwarnings("ignore")

app = FastAPI()
print("Loading Silero Model")
vad_model = load_silero_vad()

# audio queues
audio_queue = queue.Queue()
audio_queue_buffer = []
audio_stitch_timer = Timer(c.SILENCE_THRESHOLD_MS / 1000, stitch_audio_bytes, audio_queue, audio_queue_buffer)

# whisper model
try:
    print("Loading Whisper model on GPU")
    whisper_model = WhisperModel("medium", device="cuda", compute_type="float16")
except Exception as e:
    print("Loading Whisper model on CPU")
    whisper_model = WhisperModel("base", device="cpu", compute_type="int8_float16")
transcription_thread = threading.Thread(target=transcribe_audio, args=(whisper_model, audio_queue), daemon=True)
transcription_thread.start()

print("Websocket server listening")
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