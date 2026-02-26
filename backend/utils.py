import asyncio

async def push_alternating_messages(websocket):
    messages = ["start ts", "end ts"]
    index = 0
    
    try:
        while True:
            await websocket.send_text(messages[index])
            index = 1 - index 
            await asyncio.sleep(5)
    except Exception as e:
        print(f"Background task stopped: {e}")
