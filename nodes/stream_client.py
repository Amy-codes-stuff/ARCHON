import asyncio
import json

import websockets


async def receive_sensor_stream():
    uri = "ws://localhost:8000"

    print("[CLIENT] Connecting to ARCHON sensor stream...")

    async with websockets.connect(uri) as websocket:
        print("[CLIENT] Connected")
        print("[CLIENT] Receiving live sensor data...\n")

        while True:
            message = await websocket.recv()
            data = json.loads(message)

            print(
                f"[LIVE DATA] "
                f"{data['node_id']} | "
                f"Temperature: {data['temperature']}°C | "
                f"Humidity: {data['humidity']}% | "
                f"Soil Moisture: {data['soil_moisture']}%"
            )


if __name__ == "__main__":
    asyncio.run(receive_sensor_stream())
