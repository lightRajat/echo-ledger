import asyncio
import constants as c

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

async def stitch_audio_bytes(audio_queue, audio_queue_buffer: list):
    audio_length = len(audio_queue_buffer) * c.BATCH_SIZE / c.SAMPLE_RATE * 1000
    if audio_length >= c.MIN_AUDIO_LENGTH_MS :
        full_audio = b''.join(audio_queue_buffer)
        audio_queue.put(full_audio)
        audio_queue_buffer.clear()
