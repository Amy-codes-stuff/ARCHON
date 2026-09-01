import asyncio
import websockets


HOST = "0.0.0.0"
PORT = 9000


connected_peers = set()


async def signaling_handler(websocket):
    connected_peers.add(websocket)

    print("[SIGNALING] Peer connected")

    try:
        async for message in websocket:
            print(f"[SIGNALING] Message received: {message[:100]}")

            # Forward signaling messages to the other connected peer.
            for peer in connected_peers:
                if peer != websocket:
                    await peer.send(message)

    except websockets.exceptions.ConnectionClosed:
        print("[SIGNALING] Peer disconnected")

    finally:
        connected_peers.discard(websocket)


async def main():
    print("=" * 50)
    print("       ARCHON - WEBRTC SIGNALING SERVER")
    print("=" * 50)
    print(f"Host   : {HOST}")
    print(f"Port   : {PORT}")
    print("Status : ONLINE")
    print("=" * 50)

    async with websockets.serve(signaling_handler, HOST, PORT):
        print("[SIGNALING] Waiting for WebRTC peers...")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
