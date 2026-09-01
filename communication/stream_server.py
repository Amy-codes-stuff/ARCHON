import asyncio
import json
import random
from datetime import datetime

import websockets


HOST = "0.0.0.0"
PORT = 8000


async def sensor_stream(websocket):
    print("[STREAM] Client connected")

    try:
        while True:
            sensor_data = {
                "node_id": "ZONE_A",
                "timestamp": datetime.now().isoformat(),
                "temperature": round(random.uniform(24.0, 32.0), 2),
                "humidity": round(random.uniform(45.0, 75.0), 2),
                "soil_moisture": round(random.uniform(30.0, 70.0), 2)
            }

            await websocket.send(json.dumps(sensor_data))

            print(f"[STREAM SENT] {sensor_data}")

            await asyncio.sleep(2)

    except websockets.exceptions.ConnectionClosed:
        print("[STREAM] Client disconnected")


async def main():
    print("=" * 50)
    print("       ARCHON - SENSOR STREAM SERVER")
    print("=" * 50)
    print(f"Host   : {HOST}")
    print(f"Port   : {PORT}")
    print("Status : ONLINE")
    print("=" * 50)

    async with websockets.serve(sensor_stream, HOST, PORT):
        print("[STREAM] Waiting for clients...")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
