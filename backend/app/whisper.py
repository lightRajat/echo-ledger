from faster_whisper import WhisperModel
import numpy as np
import threading

class Whisper:
    def __init__(self, audio_queue, beam_size=5, language="en"):
        self.audio_queue = audio_queue
        self.beam_size = beam_size
        self.language = language
        try:
            self.model = WhisperModel("medium", device="cuda", compute_type="float16")
        except Exception as e:
            self.model = WhisperModel("base", device="cpu", compute_type="int8_float16")
        
        thread = threading.Thread(target=self.transcribe, daemon=True)
        thread.start()
        

    def transcribe(self):
        while True:
            try:
                audio_bytes = self.audio_queue.get()
                audio_np = np.frombuffer(audio_bytes, dtype=np.float32)
                segments, info = self.model.transcribe(audio_np, beam_size=self.beam_size, language=self.language)
                for segment in segments:
                    print(segment.text, end=' ')
                print()
            except Exception as e:
                print(f"Transcription Error: {e}")
            finally:
                self.audio_queue.task_done()