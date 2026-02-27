from app.db import Database
from app.utils import log, check_fuzzy_search
from huggingface_hub import hf_hub_download
import json
import llama_cpp
import threading

class Llama:
    def __init__(self, text_queue, repo_id: str, file_name: str, n_ctx: int = 512, n_gpu_layers: int = 10):
        log("Initializing Llama model...")

        thread = threading.Thread(target=self.init, args=(text_queue, repo_id, file_name, n_ctx, n_gpu_layers), daemon=True)
        thread.start()
        
    def init(self, text_queue, repo_id: str, file_name: str, n_ctx, n_gpu_layers):
        model_path = hf_hub_download(repo_id=repo_id, filename=file_name)
        self.llm = llama_cpp.Llama(
            model_path=model_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            verbose=False
        )
        self.text_queue = text_queue
        self.db = Database()
        self.products = self.db.get_all_products_name()

        with open('data/prompt.md', 'r') as f:
            self.system_message = f.read()
        
        self.monitor_conversation()

    def monitor_conversation(self):
        while True:
            text = self.text_queue.get()
            log(f"💬: {text}")
            try:
                if not self.db.transaction_running:
                    if check_fuzzy_search(text, "start transaction"):
                        self.db.start_transaction()

                if self.db.transaction_running:
                    self.extract_and_update(text)

                    if check_fuzzy_search(text, "stop transaction"):
                        self.db.stop_transaction()
            except Exception as e:
                print(f"Error in monitor loop: {e}")
            finally:
                self.text_queue.task_done()
    
    def extract_and_update(self, text: str):
        if not any(word in text for word in self.products):
            return
        
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": f"Speech fragment: {text}"},
            ],
            temperature=0,
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "product": {"type": "string"},
                            "qty": {"type": "integer"},
                            "price_hint": {"type": ["integer", "null"]},
                        },
                        "required": ["product", "qty", "price_hint"],
                    },
                },
            },
        )

        raw_json = response["choices"][0]["message"]["content"]
        data = json.loads(raw_json)
        log(f"🤖 LLM Response: {data}")

        if len(data) != 0:
            for product in data:
                self.db.process_item(product)