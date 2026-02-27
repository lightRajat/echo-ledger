from app.utils import log, check_fuzzy_search
from huggingface_hub import hf_hub_download
import json
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

        with open('data/prompt.md', 'r') as f:
            self.system_message = f.read()

    def monitor_conversation(self):
        while True:
            text = self.text_queue.get()
            log(f"Text: {text}", debug=True)
            try:
                if not self.transaction_running:
                    if check_fuzzy_search(text, "start transaction"):
                        self.transaction_running = True
                        log("✅ Transaction started.")

                if self.transaction_running:
                    self.extract_and_update(text)

                    if check_fuzzy_search(text, "stop transaction"):
                        self.transaction_running = False
                        log("🛑 Transaction stopped.")
            except Exception as e:
                print(f"Error in monitor loop: {e}")
            finally:
                self.text_queue.task_done()
    
    def extract_and_update(self, text: str):
        catalog = ["apple", "banana", "milk", "bread", "eggs", "cheese", "coffee", "tea", "sugar", "salt"]
    
        if not any(word in text for word in catalog):
            return
        
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": text},
            ],
            temperature=0,
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "item": {"type": "string"},
                            "qty": {"type": "integer"}
                        },
                        "required": ["item", "qty"]
                    }
                }
            },
        )

        raw_json = response["choices"][0]["message"]["content"]
        log(f"Response: {raw_json}", debug=True)
        data = json.loads(raw_json)

        if len(data) != 0:
            for item in data:
                log(f"{item['item']} - {item['qty']}")