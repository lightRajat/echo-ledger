from app.utils import log, check_fuzzy_search
from huggingface_hub import hf_hub_download
import llama_cpp
import threading

class Llama:
    def __init__(self, text_queue, repo_id: str, file_name: str, n_ctx: int = 512, n_gpu_layers: int = 10):
        log("Initializing Llama model...")

        model_path = hf_hub_download(repo_id=repo_id, filename=file_name)
        self.llm = llama_cpp.Llama(
            model_path=model_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            verbose=False
        )
        self.transaction_running = False
        self.text_queue = text_queue

        thread = threading.Thread(target=self.monitor_conversation, daemon=True)
        thread.start()

    def monitor_conversation(self):
        while True:
            text = self.text_queue.get()
            if self.transaction_running:
                is_ts_stopped = check_fuzzy_search(text, "stop transaction")
                if is_ts_stopped:
                    self.transaction_running = False
                    print("🛑 Transaction stopped.")
            else:
                is_ts_started = check_fuzzy_search(text, "start transaction")
                if is_ts_started:
                    self.transaction_running = True
                    print("✅ Transaction started.")
            self.text_queue.task_done()