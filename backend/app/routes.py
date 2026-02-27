from app.dashboard import Dashboard
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()
    silero = websocket.app.state.silero

    try:
        while True:
            websocket_bytes = await websocket.receive_bytes()
            silero.process_audio(websocket_bytes)

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Error: {e}")

@router.websocket("/dashboard")
async def dashboard(websocket: WebSocket):
    await websocket.accept()
    Dashboard.register_websocket(websocket)
    Dashboard.init_dashboard()

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Error: {e}")