from app.config import SAMPLE_RATE, SILENCE_THRESHOLD_MS, BATCH_SIZE, MIN_AUDIO_LENGTH_MS
from app.utils import log
import asyncio
import queue
from silero_vad import load_silero_vad
import torch

class Timer:
    def __init__(self, timeout, callback, *args, **kwargs):
        self.timeout = timeout
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.task = None

    async def _job(self):
        try:
            await asyncio.sleep(self.timeout)
            await self.callback(*self.args, **self.kwargs)
        except asyncio.CancelledError:
            pass

    def start(self):
        self.task = asyncio.create_task(self._job())

    def reset(self):
        if self.task:
            self.task.cancel()
        self.start()

    def cancel(self):
        if self.task:
            self.task.cancel()

class Silero:
    def __init__(self):
        log("Initializing Silero VAD...")

        self.vad_model = load_silero_vad()
        self.audio_queue_buffer = []
        self.audio_queue = queue.Queue()
        self.audio_stitch_timer = Timer(SILENCE_THRESHOLD_MS / 1000, self.stitch_audio_bytes)
    
    def process_audio(self, audio_bytes):
        torch_tensor = torch.frombuffer(audio_bytes, dtype=torch.float32)
        speech_prob = self.vad_model(torch_tensor, SAMPLE_RATE).item()
        if speech_prob > 0.5:
            self.audio_queue_buffer.append(audio_bytes)
            self.audio_stitch_timer.reset()
    
    async def stitch_audio_bytes(self):
        audio_length = len(self.audio_queue_buffer) * BATCH_SIZE / SAMPLE_RATE * 1000
        if audio_length >= MIN_AUDIO_LENGTH_MS :
            full_audio = b''.join(self.audio_queue_buffer)
            self.audio_queue.put(full_audio)
            self.audio_queue_buffer.clear()