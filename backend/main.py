from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

@app.websocket("/")
async def home(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    
    try:
        while True:
            websocket_bytes = await websocket.receive_bytes()
            print(f"Received audio chunk: {len(websocket_bytes)} bytes")

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)