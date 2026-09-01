import asyncio
import json

import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription


SIGNALING_URL = "ws://localhost:9000"


async def run_receiver():
    peer = RTCPeerConnection()

    @peer.on("connectionstatechange")
    async def on_connectionstatechange():
        print(f"[WEBRTC] Connection state: {peer.connectionState}")

    @peer.on("track")
    def on_track(track):
        print(f"[WEBRTC] Media track received: {track.kind}")
        print("[WEBRTC] Zone B is receiving the archaeological camera stream.")

    async with websockets.connect(SIGNALING_URL) as signaling:

        print("[WEBRTC] Zone B connected to signaling server.")
        print("[WEBRTC] Waiting for Zone A offer...")

        while True:
            raw_message = await signaling.recv()
            message = json.loads(raw_message)

            if message["type"] == "offer":

                print("[WEBRTC] Offer received from Zone A.")

                offer = RTCSessionDescription(
                    sdp=message["sdp"],
                    type="offer"
                )

                await peer.setRemoteDescription(offer)

                answer = await peer.createAnswer()
                await peer.setLocalDescription(answer)

                response = {
                    "type": "answer",
                    "sdp": peer.localDescription.sdp
                }

                await signaling.send(json.dumps(response))

                print("[WEBRTC] Answer sent to Zone A.")
                print("[WEBRTC] Waiting for media stream...")

                await asyncio.sleep(10)
                break

    await peer.close()
    print("[WEBRTC] Receiver connection closed.")


if __name__ == "__main__":
    asyncio.run(run_receiver())
