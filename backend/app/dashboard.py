import asyncio

class WebSocketReference:
    def __init__(self):
        self.socket = None
        self.loop = None

    def register_websocket(self, websocket):
        self.socket = websocket
        self.loop = asyncio.get_running_loop()
        
    def send_message_sync(self, data: dict):
        if self.socket and self.loop:
            asyncio.run_coroutine_threadsafe(self.socket.send_json(data), self.loop)
    
    def init_dashboard(self):
        from app.db import Database
        
        products = Database().products
        data = {
            "type": "init",
            "products": products
        }

        self.send_message_sync(data)
    
    def start_transaction(self):
        self.send_message_sync({
            "type": "start"
        })
    
    def stop_transaction(self):
        self.send_message_sync({
            "type": "stop"
        })
    
    def update_product(self, product_id: int, qty: int):
        self.send_message_sync({
            "type": "update",
            "product_id": product_id,
            "qty": qty
        })

Dashboard = WebSocketReference()