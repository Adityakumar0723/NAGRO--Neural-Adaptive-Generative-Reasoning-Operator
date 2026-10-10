"""WebSocket streaming endpoint for NAGRO 4.1 — real-time bidirectional chat."""

from __future__ import annotations
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from nagro.core.models import ChatRequest

router = APIRouter()


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_json(self, websocket: WebSocket, data: dict):
        await websocket.send_json(data)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """Real-time bidirectional chat via WebSocket."""
    await manager.connect(websocket)
    engine = websocket.app.state.engine
    conversation_id = None

    try:
        await manager.send_json(websocket, {
            "type": "connected",
            "model": "NAGRO 4.1",
            "message": "Connected to NAGRO 4.1. Send messages to chat.",
        })

        while True:
            data = await websocket.receive_text()

            try:
                payload = json.loads(data)
                message = payload.get("message", data)
                conversation_id = payload.get("conversation_id", conversation_id)
            except json.JSONDecodeError:
                message = data

            if not message.strip():
                continue

            await manager.send_json(websocket, {
                "type": "thinking",
                "message": "Processing...",
            })

            request = ChatRequest(
                message=message,
                conversation_id=conversation_id,
                stream=True,
            )

            # Stream response
            full_response = []
            async for chunk in engine.process_stream(request):
                full_response.append(chunk)
                await manager.send_json(websocket, {
                    "type": "token",
                    "content": chunk,
                })

            final_text = "".join(full_response)
            task_type = await engine.classify_task(message)
            conversation_id = conversation_id  # Keep conversation going

            await manager.send_json(websocket, {
                "type": "complete",
                "content": final_text,
                "task_type": task_type.value,
                "conversation_id": conversation_id,
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        try:
            await manager.send_json(websocket, {
                "type": "error",
                "message": str(e),
            })
        except Exception:
            pass
        manager.disconnect(websocket)
